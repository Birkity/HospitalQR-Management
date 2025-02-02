import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/'
    CHAPA_PUBLIC_KEY = os.environ.get('CHAPA_PUBLIC_KEY')
    CHAPA_SECRET_KEY = os.environ.get('CHAPA_SECRET_KEY')
    TELEBIRR_API_KEY = os.environ.get('TELEBIRR_API_KEY')