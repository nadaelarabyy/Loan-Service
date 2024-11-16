from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, FundSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Fund
class FundListCreate(generics.ListCreateAPIView):
    serializer_class = FundSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Fund.objects.filter(creator=user)
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(creator=self.request.user)
        else:
            print(serializer.errors)
class FundDelete(generics.DestroyAPIView):
    serializer_class = FundSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Fund.objects.filter(creator=user)
    
            
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

