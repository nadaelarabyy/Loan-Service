from django.urls import path
from .views import (
    CreateUserView,
    LoanFundTypeListView,
    LoanFundCreateView,
    LoanFundListView,
    LoanFundTypeCreateView,
    LoanTypeCreateView,
    LoanStatusChangeView,
    ActiveLoanListView,
    PendingLoanListView,
    LoanTypeListView,
    LoanRequestView,
    LoanStatusView,
    AmortizationTableView
)

urlpatterns = [
    # User registration
    path('user/register/', CreateUserView.as_view(), name='user-register'),

    # Loan Fund Type related URLs (Loan Provider)
    path('loan-fund-types/', LoanFundTypeListView.as_view(), name='loan-fund-type-list'),  # View loan fund types based on amount
    path('loan-fund/add/', LoanFundCreateView.as_view(), name='loan-fund-add'),  # Add loan fund
    path('provider/funds/', LoanFundListView.as_view(), name='loan-fund-provider-list'),  # View my funds

    # Loan Fund Type Creation (Bank Personnel)
    path('loan-fund-type/create/', LoanFundTypeCreateView.as_view(), name='loan-fund-type-create'),  # Add loan fund type

    # Loan Type Creation (Bank Personnel)
    path('loan-type/create/', LoanTypeCreateView.as_view(), name='loan-type-create'),  # Create loan type

    # Loan Status Change (Bank Personnel)
    path('loan/status/change/<int:id>/', LoanStatusChangeView.as_view(), name='loan-status-change'),  # Change loan status

    # Active Loans & Pending Loans (Bank Personnel)
    path('loan/active/', ActiveLoanListView.as_view(), name='loan-active-list'),  # View active loans
    path('loan/pending/', PendingLoanListView.as_view(), name='loan-pending-list'),  # View pending loans

    # Loan Type related URLs (Customer)
    path('loan-types/', LoanTypeListView.as_view(), name='loan-type-list'),  # View loan types based on amount

    # Loan Request (Customer)
    path('loan/request/', LoanRequestView.as_view(), name='loan-request'),  # Request loan

    # Loan Status View (Customer)
    path('loan/status/<int:id>/', LoanStatusView.as_view(), name='loan-status'),  # View loan status

    # Amortization Table (Customer)
    path('loan/amortization/<int:id>/', AmortizationTableView.as_view(), name='loan-amortization'),  # View amortization table
]
