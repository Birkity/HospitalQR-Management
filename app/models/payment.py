from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from ..config import Config

client = MongoClient(Config.MONGODB_URI)
db = client.hospital_db

class Payment:
    def __init__(self, appointment_id, amount, payment_method, status, transaction_id):
        self.appointment_id = appointment_id
        self.amount = amount
        self.payment_method = payment_method
        self.status = status
        self.transaction_id = transaction_id

    def save_to_db(self):
        return db.payments.insert_one(self.__dict__).inserted_id

    @staticmethod
    def find_by_transaction_id(transaction_id):
        return db.payments.find_one({"transaction_id": transaction_id})