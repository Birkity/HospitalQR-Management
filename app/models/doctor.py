from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
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
        return list(db.doctors.find())