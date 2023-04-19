import uuid
import requests
import environ as env

class PaymentProcessor:
    def __init__(self, secret_key):
        self.secret_key = 'sk_test_8bf0c5575575a946142b892294b33cc28dbf57f9'

    def initialize_payment(self, email, amount):
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'email': email,
            'amount': amount * 100
        }
        response = requests.post(url, headers=headers, json=payload)
        data=response.json()
        return data['data']['authorization_url']
    
    def verify_payment(self, reference):
        url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json'
        }
        response=requests.get(url, headers=headers)
        data= response.json()
        return data["data"]["status"]
        