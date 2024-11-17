from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import CustomUser, LoanFundType, LoanFund, LoanType, Loan
from django.utils import timezone
from decimal import Decimal

class LoanServiceTests(APITestCase):
    def setUp(self):
        # Create users with different roles
        self.provider_user = CustomUser.objects.create_user(
            username='provider_user',
            password='password123',
            role='provider'
        )
        self.personnel_user = CustomUser.objects.create_user(
            username='personnel_user',
            password='password123',
            role='personnel'
        )
        self.customer_user = CustomUser.objects.create_user(
            username='customer_user',
            password='password123',
            role='customer'
        )

        # Create sample Loan Fund Type and Loan Type
        self.loan_fund_type = LoanFundType.objects.create(
            min=1000,
            max=50000,
            interest_rate=5.0,
            duration=12
        )
        self.loan_type = LoanType.objects.create(
            min=1000,
            max=50000,
            interest_rate=4.5,
            duration=24
        )

        # Create client for API requests
        self.client = APIClient()

    # Test Create User
    def test_create_user(self):
        url = reverse('user-register')  # Replace with actual URL name
        data = {
            "username": "testuser",
            "password": "password123",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "role": "customer"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            f"Failed to create user: {response.data}"
        )
        self.assertEqual(
            response.data['username'], 
            "testuser", 
            "Username in response does not match the input."
        )

    # Test Loan Fund Type List (Provider)
    def test_loan_fund_type_list(self):
        self.client.force_authenticate(user=self.provider_user)
        url = reverse('loan-fund-type-list')  # Replace with actual URL name
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 
            status.HTTP_200_OK, 
            f"Loan Fund Type list failed: {response.data}"
        )
        self.assertGreaterEqual(
            len(response.data), 
            1, 
            "Loan Fund Type list returned an empty result."
        )

    # Test Loan Fund Create (Provider)
    def test_create_loan_fund(self):
        self.client.force_authenticate(user=self.provider_user)
        url = reverse('loan-fund-add')  # Replace with actual URL name
        data = {
            "provider": self.provider_user.id,  # Pass provider ID
            "amount": 20000,
            "loanFundType": self.loan_fund_type.id  # Pass loanFundType ID
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            f"Failed to create loan fund: {response.data}"
        )

    # Test Loan Request (Customer)
    def test_request_loan(self):
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('loan-request')  # Replace with actual URL name
        data = {
            "customer": self.customer_user.id,  # Pass customer ID
            "amount": 15000,
            "loanType": self.loan_type.id  # Pass loanType ID
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            f"Failed to request loan: {response.data}"
        )

    # Test Loan Status View (Customer)
    def test_loan_status_view(self):
        loan = Loan.objects.create(
            customer=self.customer_user,
            amount=15000,
            loanType=self.loan_type,
            status='pending'
        )
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('loan-status', kwargs={'id': loan.id})  # Replace with actual URL name
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Failed to fetch loan status: {response.data}"
        )

    # Test Amortization Table View (Customer)
    def test_amortization_table_view(self):
        loan = Loan.objects.create(
            customer=self.customer_user,
            amount=15000,
            loanType=self.loan_type,
            status='approved'
        )
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('loan-amortization', kwargs={'id': loan.id})  # Replace with actual URL name
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Failed to fetch amortization table: {response.data}"
        )
        self.assertIn(
            'amortization_table',
            response.data,
            "Amortization table missing in response."
        )

    # Test Active Loans List (Personnel)
    def test_active_loans_list(self):
        Loan.objects.create(
            customer=self.customer_user,
            amount=15000,
            loanType=self.loan_type,
            status='approved'
        )
        self.client.force_authenticate(user=self.personnel_user)
        url = reverse('loan-active-list')  # Replace with actual URL name
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Failed to fetch active loans: {response.data}"
        )

    # Test Pending Loans List (Personnel)
    def test_pending_loans_list(self):
        Loan.objects.create(
            customer=self.customer_user,
            amount=15000,
            loanType=self.loan_type,
            status='pending'
        )
        self.client.force_authenticate(user=self.personnel_user)
        url = reverse('loan-pending-list')  # Replace with actual URL name
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 
            status.HTTP_200_OK, 
            f"Failed to fetch pending loans: {response.data}"
        )
