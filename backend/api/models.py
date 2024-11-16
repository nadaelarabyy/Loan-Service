from django.db import models
from django.contrib.auth.models import User

class Fund(models.Model):
    min = models.BigIntegerField()
    max = models.BigIntegerField()
    interest = models.DecimalField(max_digits=5, decimal_places=2)
    duration = models.PositiveIntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="funds") 
    
    def __str__(self) -> str:
        return super().__str__()
