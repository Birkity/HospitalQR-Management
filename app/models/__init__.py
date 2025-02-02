from .user import User
from .appointment import Appointment
from .doctor import Doctor
from .payment import Payment
from .patient import Patient
from .doctor import db  # Import the db object

__all__ = ['User', 'Appointment', 'Doctor', 'Payment', 'Patient', 'db']