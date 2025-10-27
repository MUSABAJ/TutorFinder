import requests
import json
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

class ChapaPayment:
    def __init__(self):
        self.secret_key = getattr(settings, 'CHAPA_SECRET_KEY')
        self.base_url = getattr(settings, 'CHAPA_BASE_URL', 'https://api.chapa.co/v1')
        
        if not self.secret_key:
            raise ImproperlyConfigured("CHAPA_SECRET_KEY is not set in settings")
    
    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json'
        }
    
    def initialize_transaction(self, email, amount, tx_ref, first_name, last_name, callback_url=None):
        """Initialize payment to platform account"""
        url = "https://api.chapa.co/v1/transaction/initialize"
        payload = {
            "amount": str(amount),
            "currency": "ETB",
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "tx_ref": tx_ref,
            "callback_url": callback_url,
            "customization": {
                "title": "Tutor Sessio",
                "description": "Payment held by platform until session completion"
            }
        }
        
        try:
            response = requests.post(url, headers=self.get_headers(), data=json.dumps(payload))
            data = response.text
            print(data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Chapa API Error: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response content: {e.response.text}")
            return None
    
    def verify_transaction(self, tx_ref):
        """Verify transaction status"""
        url = f"{self.base_url}/transaction/verify/{tx_ref}"
        
        try:
            response = requests.get(url, headers=self.get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Chapa Verification Error: {e}")
            return None
    
    def transfer_to_bank(self, account_number, amount, reference, bank_code, account_name=None):
        """Transfer funds from platform account to tutor's bank account"""
        url = f"{self.base_url}/transfer"
        
        payload = {
            "account_number": account_number,
            "amount": str(amount),
            "currency": "ETB",
            "reference": reference,
            "bank_code": bank_code
        }
        
        if account_name:
            payload["account_name"] = account_name
        
        try:
            response = requests.post(url, headers=self.get_headers(), data=json.dumps(payload))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Chapa Transfer Error: {e}")
            return None
    
    def refund_transaction(self, transaction_id, amount, reason="Session refund"):
        """Refund payment back to student"""
        url = f"{self.base_url}/refund"
        
        payload = {
            "transaction_id": transaction_id,
            "amount": str(amount),
            "currency": "ETB",
            "reason": reason
        }
        
        try:
            response = requests.post(url, headers=self.get_headers(), data=json.dumps(payload))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Chapa Refund Error: {e}")
            return None