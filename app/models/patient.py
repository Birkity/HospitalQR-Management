from pymongo import MongoClient
from ..config import Config
from datetime import datetime
from bson import ObjectId
import qrcode
import base64
from io import BytesIO

client = MongoClient(Config.MONGODB_URI)
db = client.hospital_db

class Patient:
    def __init__(self, name, email, phone, date_of_birth, user_id=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.date_of_birth = date_of_birth
        self.user_id = user_id
        self.registration_date = datetime.now()

    def save_to_db(self):
        return db.patients.insert_one(self.__dict__).inserted_id

    @staticmethod
    def find_all():
        return db.patients.find()

    @staticmethod
    def initialize_dummy_data():
        if db.patients.count_documents({}) == 0:  # Check if collection is empty
            print("Initializing dummy patient data...")  # Debugging statement
            dummy_patients = [
                {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "phone": "+251911111111",
                    "date_of_birth": "1990-01-01",
                    "registration_date": datetime.now()
                },
                {
                    "name": "Jane Smith",
                    "email": "jane@example.com",
                    "phone": "+251922222222",
                    "date_of_birth": "1992-05-15",
                    "registration_date": datetime.now()
                }
            ]
            db.patients.insert_many(dummy_patients)
            print("Dummy patient data initialized")

    def generate_qr_code(self):
        """Generate QR code containing patient information"""
        patient_data = {
            'id': str(self._id),
            'name': self.name,
            'email': self.email
        }
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(str(patient_data))
        qr.make(fit=True)

        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for displaying in HTML
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"

    @staticmethod
    def find_by_id(patient_id):
        if isinstance(patient_id, str):
            patient_id = ObjectId(patient_id)
        return db.patients.find_one({'_id': patient_id})

    @classmethod
    def create_from_user(cls, user):
        """Create a patient record from a user account"""
        patient = cls(
            name=user.name,
            email=user.email,
            phone="",  # Can be updated later
            date_of_birth="",  # Can be updated later
            user_id=str(user._id)
        )
        patient_id = patient.save_to_db()
        patient._id = patient_id  # Set the _id after saving to the database
        return patient_id

    @staticmethod
    def find_by_user_id(user_id):
        """Find patient by associated user ID"""
        if isinstance(user_id, str):
            patient_data = db.patients.find_one({'user_id': user_id})
            if patient_data:
                patient = Patient(
                    name=patient_data['name'],
                    email=patient_data['email'],
                    phone=patient_data.get('phone', ''),
                    date_of_birth=patient_data.get('date_of_birth', ''),
                    user_id=patient_data['user_id']
                )
                patient._id = patient_data['_id']  # Set the _id from the database
                return patient
        return None 