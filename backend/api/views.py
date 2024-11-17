from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from decimal import Decimal
from rest_framework import generics, permissions
from .models import LoanFundType, LoanFund, LoanType, Loan, CustomUser
from .serializers import LoanFundTypeSerializer, LoanFundSerializer, LoanTypeSerializer, LoanSerializer, CustomUserSerializer
from .permissions import IsProvider, IsPersonnel, IsCustomer  # Custom permissions
from rest_framework.response import Response


class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
    def perform_create(self, serializer):
        self.user = serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "role": self.user.role,
        }
        return response


# Loan Fund Type Views (For Loan Providers)
class LoanFundTypeListView(generics.ListAPIView):
    queryset = LoanFundType.objects.all()
    serializer_class = LoanFundTypeSerializer
    permission_classes = [IsProvider]

    def get_queryset(self):
        """
        Filter loan fund types based on the provided amount.
        Loan providers can view loan fund types based on the amount.
        """
        amount = self.request.query_params.get('amount')
        if amount:
            return LoanFundType.objects.filter(min__lte=amount, max__gte=amount)
        return LoanFundType.objects.all()


class LoanFundCreateView(generics.CreateAPIView):
    queryset = LoanFund.objects.all()
    serializer_class = LoanFundSerializer
    permission_classes = [IsProvider]


class LoanFundListView(generics.ListAPIView):
    serializer_class = LoanFundSerializer
    permission_classes = [IsProvider]

    def get_queryset(self):
        """
        Loan provider views their funds (related to them).
        """
        user = self.request.user
        return LoanFund.objects.filter(provider=user)


# Bank Personnel Views
class LoanFundTypeCreateView(generics.CreateAPIView):
    queryset = LoanFundType.objects.all()
    serializer_class = LoanFundTypeSerializer
    permission_classes = [IsPersonnel]


class LoanTypeCreateView(generics.CreateAPIView):
    queryset = LoanType.objects.all()
    serializer_class = LoanTypeSerializer
    permission_classes = [IsPersonnel]


class LoanStatusChangeView(generics.UpdateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsPersonnel]
    lookup_field = 'id'

    def perform_update(self, serializer):
        loan = self.get_object()
        new_status = self.request.data.get('status')
        if new_status:
            loan.status = new_status
        serializer.save()


class ActiveLoanListView(generics.ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsPersonnel]

    def get_queryset(self):
        """
        Bank Personnel can view all active loans.
        """
        return Loan.objects.filter(status='approved')
class PendingLoanListView(generics.ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsPersonnel]

    def get_queryset(self):
        """
        Bank Personnel can view all pending loans.
        """
        return Loan.objects.filter(status='pending')


# Customer Views
class LoanTypeListView(generics.ListAPIView):
    queryset = LoanType.objects.all()
    serializer_class = LoanTypeSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        """
        Customer can view loan types based on amount.
        """
        amount = self.request.query_params.get('amount')
        if amount:
            return LoanType.objects.filter(min__lte=amount, max__gte=amount)
        return LoanType.objects.all()


class LoanRequestView(generics.CreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsCustomer]

    def perform_create(self, serializer):
        # Link the loan request with the logged-in customer
        serializer.save(customer=self.request.user)


class LoanStatusView(generics.RetrieveAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsCustomer]
    lookup_field = 'id'

    def get_queryset(self):
        """
        Customer can view the status of their loan.
        """
        return Loan.objects.filter(customer=self.request.user)


class AmortizationTableView(generics.GenericAPIView):
    serializer_class = LoanSerializer
    permission_classes = [IsCustomer]
    queryset = Loan.objects.all()  # Add this to define the queryset

    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        loan = self.get_object()
        amortization_table = self.generate_amortization_table(loan)
        return Response({"amortization_table": amortization_table})

    def generate_amortization_table(self, loan):
        # Loan details
        principal = Decimal(loan.amount)  # Ensure principal is a Decimal
        annual_interest_rate = Decimal(loan.loanType.interest_rate)  # Ensure interest rate is a Decimal
        months = loan.loanType.duration  # Loan duration in months

        # Monthly interest rate (annual interest rate / 12)
        monthly_interest_rate = annual_interest_rate / Decimal(12)

        amortization_schedule = []
        remaining_balance = principal

        for month in range(1, months + 1):
            # Interest payment for the current month
            interest_payment = remaining_balance * monthly_interest_rate if monthly_interest_rate > 0 else Decimal(0)
            
            # Principal payment is the total monthly payment minus the interest payment
            total_payment = principal / Decimal(months) if monthly_interest_rate == 0 else interest_payment + (principal / months)
            
            principal_payment = total_payment - interest_payment

            # Ensure the last payment clears the remaining balance
            if month == months:
                principal_payment = remaining_balance

            # Update the remaining balance
            remaining_balance -= principal_payment

            # Add the month data to the amortization table
            amortization_schedule.append({
                "month": month,
                "principal_payment": round(principal_payment, 2),
                "interest_payment": round(interest_payment, 2),
                "total_payment": round(total_payment, 2),
                "remaining_balance": round(remaining_balance, 2)
            })

        return amortization_schedule


