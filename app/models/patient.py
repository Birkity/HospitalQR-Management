from pymongo import MongoClient
from ..config import Config
from datetime import datetime

client = MongoClient(Config.MONGODB_URI)
db = client.hospital_db

class Patient:
    def __init__(self, name, email, phone, date_of_birth):
        self.name = name
        self.email = email
        self.phone = phone
        self.date_of_birth = date_of_birth
        self.registration_date = datetime.now()

    def save_to_db(self):
        return db.patients.insert_one(self.__dict__).inserted_id

    @staticmethod
    def find_all():
        return db.patients.find()

    @staticmethod
    def initialize_dummy_data():
        if db.patients.count_documents({}) == 0:  # Check if collection is empty
            dummy_patients = [
                {
                    "name": "John Smith",
                    "email": "john.smith@example.com",
                    "phone": "+251911111111",
                    "date_of_birth": "1990-05-15",
                    "registration_date": datetime.now()
                },
                {
                    "name": "Sarah Johnson",
                    "email": "sarah.j@example.com",
                    "phone": "+251922222222",
                    "date_of_birth": "1985-08-22",
                    "registration_date": datetime.now()
                },
                {
                    "name": "Michael Brown",
                    "email": "michael.b@example.com",
                    "phone": "+251933333333",
                    "date_of_birth": "1978-12-10",
                    "registration_date": datetime.now()
                },
                {
                    "name": "Emma Wilson",
                    "email": "emma.w@example.com",
                    "phone": "+251944444444",
                    "date_of_birth": "1995-03-28",
                    "registration_date": datetime.now()
                },
                {
                    "name": "David Lee",
                    "email": "david.lee@example.com",
                    "phone": "+251955555555",
                    "date_of_birth": "1982-07-14",
                    "registration_date": datetime.now()
                }
            ]
            db.patients.insert_many(dummy_patients)

    @staticmethod
    def find_by_id(patient_id):
        return db.patients.find_one({'_id': patient_id}) 