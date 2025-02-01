from pymongo import MongoClient
from ..config import Config

client = MongoClient(Config.MONGODB_URI)
db = client.hospital_db

class Doctor:
    def __init__(self, name, specialty, availability):
        self.name = name
        self.specialty = specialty
        self.availability = availability

    def save_to_db(self):
        return db.doctors.insert_one(self.__dict__).inserted_id

    @staticmethod
    def list_all():
        return db.doctors.find()

    @staticmethod
    def initialize_dummy_data():
        if db.doctors.count_documents({}) == 0:  # Check if the collection is empty
            dummy_doctors = [
                {"name": "Dr. John Doe", "specialty": "Cardiology", "availability": "MWF"},
                {"name": "Dr. Jane Smith", "specialty": "Neurology", "availability": "TTh"},
                {"name": "Dr. Emily Johnson", "specialty": "Pediatrics", "availability": "MWF"},
                {"name": "Dr. Michael Brown", "specialty": "Orthopedics", "availability": "TTh"},
                {"name": "Dr. Sarah Davis", "specialty": "Dermatology", "availability": "MWF"},
                {"name": "Dr. David Wilson", "specialty": "Oncology", "availability": "TTh"},
                {"name": "Dr. Laura Martinez", "specialty": "Psychiatry", "availability": "MWF"},
                {"name": "Dr. Robert Garcia", "specialty": "Radiology", "availability": "TTh"},
                {"name": "Dr. Linda Anderson", "specialty": "Gastroenterology", "availability": "MWF"},
                {"name": "Dr. James Thomas", "specialty": "Urology", "availability": "TTh"}
            ]
            db.doctors.insert_many(dummy_doctors)

# Call this function at the start of your application
Doctor.initialize_dummy_data()