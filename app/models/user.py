from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from ..config import Config

client = MongoClient(Config.MONGODB_URI)
db = client.hospital_db

class User:
    def __init__(self, username, email, password, user_type, qr_code=None):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.user_type = user_type
        self.qr_code = qr_code

    def save_to_db(self):
        user_data = self.__dict__.copy()
        del user_data['password_hash']  # Don't save the plain password
        user_data['password'] = self.password_hash
        return db.users.insert_one(user_data).inserted_id

    @staticmethod
    def find_by_email(email):
        user = db.users.find_one({"email": email})
        if user:
            user['id'] = str(user['_id'])
            del user['_id']
        return user

    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)