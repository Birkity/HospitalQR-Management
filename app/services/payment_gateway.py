import requests
from flask import current_app

class ChapaPayment:
    def __init__(self, public_key=None, secret_key=None):
        self.base_url = "https://api.chapa.co/v1"
        self.public_key = None
        self.secret_key = None

    def init_app(self, app):
        """Initialize with Flask app config"""
        self.public_key = app.config['CHAPA_PUBLIC_KEY']
        self.secret_key = app.config['CHAPA_SECRET_KEY']

    def initialize_payment(self, amount, email, first_name, last_name, tx_ref):
        if not self.secret_key:
            raise RuntimeError("Chapa Payment not initialized. Call init_app() first.")

        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "amount": amount,
            "currency": "ETB",
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "tx_ref": tx_ref,
            "callback_url": "http://localhost:5000/payment/callback",
            "return_url": "http://localhost:5000/payment/success"
        }

        response = requests.post(
            f"{self.base_url}/transaction/initialize",
            json=payload,
            headers=headers
        )
        return response.json()

    def verify_payment(self, tx_ref):
        if not self.secret_key:
            raise RuntimeError("Chapa Payment not initialized. Call init_app() first.")

        headers = {
            "Authorization": f"Bearer {self.secret_key}"
        }
        
        response = requests.get(
            f"{self.base_url}/transaction/verify/{tx_ref}",
            headers=headers
        )
        return response.json()