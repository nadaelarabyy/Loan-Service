from rest_framework.permissions import BasePermission

class IsProvider(BasePermission):
    """Allow access only to Loan Providers."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'provider'


class IsCustomer(BasePermission):
    """Allow access only to Loan Customers."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'


class IsPersonnel(BasePermission):
    """Allow access only to Bank Personnel."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'personnel'
