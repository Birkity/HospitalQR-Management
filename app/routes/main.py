import datetime
from flask import abort, render_template, redirect, session, url_for, flash, request, current_app
from . import main_bp
from ..models import User, Appointment, Doctor, Payment
from ..services import generate_qr_code
from flask import Blueprint  
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)  

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/test')
def test():
    return "Test route is working!"

@main_bp.route('/appointments', methods=['GET', 'POST'])
@login_required
def manage_appointments():
    if request.method == 'POST':
        patient_id = current_user.get_id()  # Get ID from current_user
        doctor_id = request.form['doctor_id']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        notes = request.form.get('notes', "")
        
        appointment = Appointment(patient_id, doctor_id, appointment_date, appointment_time, "scheduled", notes)
        appointment_id = appointment.save_to_db()
        
        return redirect(url_for('main.payment', appointment_id=appointment_id))
    
    doctors = Doctor.list_all()
    return render_template('appointments.html', doctors=doctors)

@main_bp.route('/payment/<appointment_id>')
def payment(appointment_id):
    return render_template('payment.html', chapa_public_key=current_app.config['CHAPA_PUBLIC_KEY'], appointment_id=appointment_id)

@main_bp.route('/payment_callback', methods=['GET', 'POST'])
def payment_callback():
    tx_ref = request.args.get('tx_ref')
    if tx_ref:
        payment = Payment.find_by_transaction_id(tx_ref)
        if payment:
            chapa = current_app.config['CHAPA_API']
            verification = chapa.verify_payment(tx_ref)
            if verification.get('status') == 'success':
                Payment.update_one({"_id": payment['_id']}, {"$set": {"status": "completed"}})
                flash('Payment successful, thank you!', 'success')
                return redirect(url_for('main.payment_success'))
            else:
                flash(f'Payment verification failed: {verification.get("message", "An error occurred.")}', 'error')
        else:
            flash('Payment not found.', 'error')
    else:
        flash('Transaction reference not provided.', 'error')
    return redirect(url_for('main.index'))

@main_bp.route('/payment_success')
def payment_success():
    return render_template('payment_success.html')

@main_bp.route('/admin')
def admin_dashboard():
    if 'user' not in session or not session['user'].get('is_admin'):
        abort(403)  # Forbidden if not admin

    try:
        patient_visits = list(Appointment.find().sort("appointment_date", -1).limit(10))
        payment_records = list(Payment.find().sort("created_at", -1).limit(10))
        doctors = Doctor.list_all()
        doctors_count = len(doctors)

        most_visited_doctor = max(doctors, key=lambda d: Appointment.count_documents({"doctor_id": str(d['_id'])}), default=None)
        if most_visited_doctor:
            most_visited_doctor['visit_count'] = Appointment.count_documents({"doctor_id": str(most_visited_doctor['_id'])})

        total_paid = sum(payment['amount'] for payment in payment_records)

        today = datetime.datetime.now()
        start_of_month = datetime.datetime(today.year, today.month, 1)
        monthly_revenue = Payment.aggregate([
            {"$match": {"status": "completed", "created_at": {"$gte": start_of_month}}},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ])
        monthly_revenue = next(monthly_revenue, {'total': 0})['total'] if monthly_revenue else 0

    except Exception as e:
        flash(f'Error fetching dashboard data: {str(e)}', 'error')
        return redirect(url_for('main.index'))

    return render_template('admin_dashboard.html', 
                           patient_visits=patient_visits,
                           payment_records=payment_records,
                           doctors=doctors,
                           doctors_count=doctors_count,
                           most_visited_doctor=most_visited_doctor,
                           total_paid=total_paid,
                           monthly_revenue=monthly_revenue)

@main_bp.route('/profile')
def profile():
    user = User.find_by_email('current_user_email') 
    qr_code = generate_qr_code(user['qr_code'])
    return render_template('profile.html', qr_code=qr_code)