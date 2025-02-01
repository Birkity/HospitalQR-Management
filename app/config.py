import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/hospital_db')
    CHAPA_PUBLIC_KEY = os.getenv('CHAPA_PUBLIC_KEY')
    CHAPA_SECRET_KEY = os.getenv('CHAPA_SECRET_KEY')