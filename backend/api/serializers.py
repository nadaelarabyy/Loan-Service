from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Fund

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = ["id", "min", "max", "interest", "duration", "creator"]
        extra_kwargs = {"creator": {"read_only":True}}
