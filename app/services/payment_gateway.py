import requests
from ..config import Config

class ChapaPayment:
    def __init__(self):
        self.base_url = "https://api.chapa.co/v1"
        self.headers = {
            "Authorization": f"Bearer {Config.CHAPA_SECRET_KEY}",
            "Content-Type": "application/json"
        }

    def verify_payment(self, tx_ref):
        response = requests.get(f"{self.base_url}/transaction/verify/{tx_ref}", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {'status': 'error', 'message': f'Verification failed with status code {response.status_code}'}