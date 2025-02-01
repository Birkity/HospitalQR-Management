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
        self.password_hash = generate_password_hash(password) if password else None
        self.role = role
        self._id = _id

    def get_id(self):
        return str(self._id)

    @staticmethod
    def create_from_db(user_data):
        """Convert a database user dictionary to a User object"""
        if user_data:
            return User(
                username=user_data.get('username'),
                email=user_data.get('email'),
                password=None,  # We don't need to pass the password here
                role=user_data.get('role'),
                _id=user_data.get('_id')
            )
        return None

    def save_to_db(self):
        user_data = {
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'role': self.role
        }
        result = db.users.insert_one(user_data)
        self._id = result.inserted_id
        return self._id

    @staticmethod
    def find_by_email(email):
        return db.users.find_one({'email': email})

    @staticmethod
    def verify_password(user_data, password):
        if not user_data or 'password_hash' not in user_data:
            return False
        return check_password_hash(user_data['password_hash'], password)

    @staticmethod
    def find_by_id(user_id):
        return db.users.find_one({'_id': user_id})