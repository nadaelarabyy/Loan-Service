from rest_framework import serializers
from .models import CustomUser, LoanFundType, LoanFund, LoanType, Loan
from django.contrib.auth.models import Group, Permission
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims (optional)
        token['email'] = user.email
        token['role'] = user.role  # Include user role if necessary
        return token

    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)

        if email is None or password is None:
            raise AuthenticationFailed("Email and password are required.")

        # Authenticate the user by email
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed("No active account found with the given credentials.")

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid email or password.")

        if not user.is_active:
            raise AuthenticationFailed("User account is disabled.")

        data = super().validate(attrs)
        refresh = self.get_token(user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data

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

