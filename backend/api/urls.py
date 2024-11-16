from django.urls import path

from . import views

urlpatterns = [
    path('funds/', views.FundListCreate.as_view(), name="fund-list"),
    path('funds/delete/<int:pk>/', views.FundDelete.as_view(), name="delete-fund")
]
