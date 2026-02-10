from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views.customer_registration import ( 
    request_registration_otp, 
    register_user, 
    me
)

from .jwt import CustomTokenObtainPairView

urlpatterns = [
    # JWT Token endpoints
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    
    # Registration
    path("request-otp/", request_registration_otp, name="request_registration_otp"),
    path("register/", register_user, name="register_user"), 

    # User profile
    path("me/", me, name="user_profile"),
]
