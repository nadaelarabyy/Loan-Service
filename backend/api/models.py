from django.db import models
from django.contrib.auth.models import User, AbstractUser, Permission, Group
from dateutil.relativedelta import relativedelta
from django.utils import timezone
# Custom User model
class CustomUser(AbstractUser):
    USER_ROLES = (
        ('provider', 'Loan Provider'),
        ('customer', 'Loan Customer'),
        ('personnel', 'Bank Personnel'),
    )
    role = models.CharField(max_length=10, choices=USER_ROLES, default='customer')
     # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        Group, 
        related_name='customuser_set',  # Custom reverse name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, 
        related_name='customuser_set',  # Custom reverse name
        blank=True
    )
    


class LoanFundType(models.Model):
    min = models.BigIntegerField()
    max = models.BigIntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    duration = models.PositiveIntegerField()  # in months
    createdAt = models.DateTimeField(auto_now=True)
    
# Loan Fund model for Loan Providers
class LoanFund(models.Model):
    provider = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'provider'})
    amount = models.PositiveIntegerField()
    loanFundType = models.ForeignKey(LoanFundType, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Ensure createdAt is set before calculating expiry_date
        if not self.createdAt:
            self.createdAt = timezone.now()
        if self.loanFundType and self.loanFundType.duration:
            self.expiry_date = self.createdAt + relativedelta(months=self.loanFundType.duration)
        super().save(*args, **kwargs)


class LoanType(models.Model):
    min = models.BigIntegerField()
    max = models.BigIntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    duration = models.PositiveIntegerField()  # in months
    createdAt = models.DateTimeField(auto_now=True)  
        
# Loan model for Loan Customers
class Loan(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    loanType = models.ForeignKey(LoanType, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    createdAt = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Ensure createdAt is set before calculating expiry_date
        if not self.createdAt:
            self.createdAt = timezone.now()  # Import timezone from django.utils
        if self.loanType and self.loanType.duration:
            self.expiry_date = self.createdAt + relativedelta(months=self.loanType.duration)
        super().save(*args, **kwargs)


