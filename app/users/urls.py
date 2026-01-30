from django.urls import path
from .views.customer_registration import request_registration_otp

urlpatterns = [
    path('request-otp/', request_registration_otp, name='request_registration_otp'),
]