from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from ..config import Config
from flask_login import UserMixin

client = MongoClient(Config.MONGODB_URI)
db = client.hospital_db

class User(UserMixin):
    def __init__(self, username, email, password, role, _id=None):
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self._id = _id

    def get_id(self):
        return str(self._id)

    @staticmethod
    def create_from_db(user_data):
        """Convert a database user dictionary to a User object"""
        return User(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            role=user_data['role'],
            _id=user_data['_id']
        )

    def save_to_db(self):
        user_data = self.__dict__.copy()
        del user_data['password']  # Don't save the plain password
        user_data['password_hash'] = generate_password_hash(self.password)
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