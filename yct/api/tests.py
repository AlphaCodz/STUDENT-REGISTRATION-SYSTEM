from django.test import TestCase, Client
from decimal import Decimal
from .models import SchoolUser, Payment

# Create your tests here.
class PaymentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = SchoolUser.objects.create(
            first_name='Test',
            last_name='User',
            email="test@example.com",
            password='password'
        )
        
    def test_payment_flow(self):
        # Make sure the user has a balance of zero
        self.assertEqual(self.user.balance, Decimal('0'))
        
        # Initialize a payment of 10000 Naira
        response = self.client.post('/initialize-payment/', {'amount':'1000'}, HTTP_AUTHORIZATION='Bearer sk_test_8bf0c5575575a946142b892294b33cc28dbf57f9')
        self.assertEqual(response.status_code, 200)
        self.assertIn('authorization_url', response.json())
        self.assertIn('payment_id', response.json())
        
        # Reload the user and make sure their balance is now 1000 naira
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, Decimal('1000'))
