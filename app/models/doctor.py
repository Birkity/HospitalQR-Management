from pymongo import MongoClient
from ..config import Config

client = MongoClient(Config.MONGODB_URI)
db = client.hospital_db

class Doctor:
    def __init__(self, name, specialty, availability=None):
        self.name = name
        self.specialty = specialty
        self.availability = availability or []  # List of available time slots

    def save_to_db(self):
        return db.doctors.insert_one(self.__dict__).inserted_id

    @staticmethod
    def list_all():
        return db.doctors.find()

    @staticmethod
    def find_by_id(doctor_id):
        return db.doctors.find_one({'_id': doctor_id})

    def update_availability(self, new_availability):
        self.availability = new_availability
        db.doctors.update_one({'_id': self._id}, {'$set': {'availability': self.availability}})

    # Remove dummy data initialization if it's causing issues