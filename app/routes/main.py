from flask import render_template, redirect, url_for, flash, request, current_app
from . import main
from ..models import User, Appointment, Doctor, Payment
from ..services import generate_qr_code

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/appointments', methods=['GET', 'POST'])
def manage_appointments():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        notes = request.form.get('notes', "")
        
        appointment = Appointment(patient_id, doctor_id, appointment_date, appointment_time, "scheduled", notes)
        appointment_id = appointment.save_to_db()
        
        return redirect(url_for('main.payment', appointment_id=appointment_id))
    
    doctors = Doctor.list_all()
    return render_template('appointments.html', doctors=doctors)

@main.route('/payment/<appointment_id>')
def payment(appointment_id):
    return render_template('payment.html', chapa_public_key=current_app.config['CHAPA_PUBLIC_KEY'], appointment_id=appointment_id)

@main.route('/payment_callback', methods=['GET', 'POST'])
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

@main.route('/payment_success')
def payment_success():
    return render_template('payment_success.html')

@main.route('/admin')
def admin_dashboard():
    # Here you would implement fetching data for admin dashboard
    return render_template('admin_dashboard.html')

@main.route('/profile')
def profile():
    # Assuming user is logged in
    user = User.find_by_email('current_user_email')  # Implement session management
    qr_code = generate_qr_code(user['qr_code'])
    return render_template('profile.html', qr_code=qr_code)