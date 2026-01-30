from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class NewCustomerOnBoardingSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    