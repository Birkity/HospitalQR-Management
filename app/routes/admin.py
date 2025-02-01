from flask import Blueprint, render_template, session, abort
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.payment import Payment
from app.models.doctor import Doctor
from datetime import datetime
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_dashboard():
    if 'user' not in session or not session['user'].get('is_admin'):
        abort(403)  # Forbidden if not admin

    patients = list(Patient.find_all())
    appointments = list(Appointment.find_all())
    payments = list(Payment.find_all())
    doctors = list(Doctor.list_all())

    # Calculate statistics
    total_patients = len(patients)
    today_appointments = sum(1 for a in appointments if a['appointment_date'].date() == datetime.now().date())
    most_visited_doctor = max(doctors, key=lambda d: sum(1 for a in appointments if a['doctor_id'] == d['_id']), default=None)

    return render_template('admin_dashboard.html',
                           patients=patients,
                           appointments=appointments,
                           payments=payments,
                           doctors=doctors,
                           total_patients=total_patients,
                           today_appointments=today_appointments,
                           most_visited_doctor=most_visited_doctor)