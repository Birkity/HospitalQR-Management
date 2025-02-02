from flask_login import UserMixin
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from ..config import Config

client = MongoClient(Config.MONGODB_URI)
db = client.hospital_db

class User(UserMixin):
    def __init__(self, email, password, name, is_admin=False):
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.name = name
        self.is_admin = is_admin
        self._id = None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save_to_db(self):
        user_data = {
            'email': self.email,
            'password_hash': self.password_hash,
            'name': self.name,
            'is_admin': self.is_admin
        }
        result = db.users.insert_one(user_data)
        self._id = result.inserted_id
        return self._id

    def get_id(self):
        if self._id:
            return str(self._id)
        return None

    @staticmethod
    def find_by_email(email):
        return db.users.find_one({'email': email})

    @staticmethod
    def find_by_id(user_id):
        if not user_id:
            return None
        try:
            if isinstance(user_id, str):
                user_id = ObjectId(user_id)
            return db.users.find_one({'_id': user_id})
        except:
            return None

    @classmethod
    def create_from_db(cls, user_data):
        user = cls(
            email=user_data['email'],
            password='',  # Password hash is already stored
            name=user_data['name'],
            is_admin=user_data.get('is_admin', False)
        )
        user.password_hash = user_data['password_hash']
        user._id = user_data['_id']
        return user