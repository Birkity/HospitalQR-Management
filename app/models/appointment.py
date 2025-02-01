from pymongo import MongoClient
from bson.objectid import ObjectId
from ..config import Config

client = MongoClient(Config.MONGODB_URI)
db = client.hospital_db

class Appointment:
    def __init__(self, patient_id, doctor_id, appointment_date, appointment_time, status, notes=""):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.status = status
        self.notes = notes
    
    def save_to_db(self):
        return db.appointments.insert_one(self.__dict__).inserted_id

    @staticmethod
    def find_by_id(appointment_id):
        return db.appointments.find_one({"_id": ObjectId(appointment_id)})