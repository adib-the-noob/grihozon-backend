from rest_framework.views import APIView
from config.responses import APIResponse
from django.contrib.auth import get_user_model

User = get_user_model()

class NewCustomerOnBoarding(APIView):
    pass