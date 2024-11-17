from rest_framework import serializers
from .models import CustomUser, LoanFundType, LoanFund, LoanType, Loan
from django.contrib.auth.models import Group, Permission


# Serializer for CustomUser model
class CustomUserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), 
        many=True, 
        required=False
    )
    user_permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), 
        many=True, 
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'groups', 'user_permissions']
        read_only_fields = ['id']


# Serializer for LoanFundType model
class LoanFundTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanFundType
        fields = ['id', 'min', 'max', 'interest_rate', 'duration', 'createdAt']
        read_only_fields = ['id', 'createdAt']


# Serializer for LoanFund model
class LoanFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanFund
        fields = ['provider', 'amount', 'loanFundType']



    class Meta:
        model = LoanFund
        fields = ['id', 'provider', 'amount', 'loanFundType', 'createdAt', 'expiry_date']
        read_only_fields = ['id', 'createdAt', 'expiry_date']


# Serializer for LoanType model
class LoanTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanType
        fields = ['id', 'min', 'max', 'interest_rate', 'duration', 'createdAt']
        read_only_fields = ['id', 'createdAt']


# Serializer for Loan model
class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['customer', 'amount', 'loanType', 'status']

