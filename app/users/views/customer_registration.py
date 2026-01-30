from rest_framework.decorators import api_view

from config.responses import APIResponse
from django.contrib.auth import get_user_model
from ..serializers.user_registration import (
    UserRegistrationOTPRequest,
    UserRegistrationSerializer,
)
from ..tasks.otp_service import send_otp

User = get_user_model()


@api_view(["POST"])
def request_registration_otp(request):
    serializer = UserRegistrationOTPRequest(data=request.data)
    if serializer.is_valid():
        existing_user = User.objects.filter(
            phone_number=serializer.validated_data["phone_number"]
        ).exists()
        if existing_user:
            return APIResponse.error(message="Phone number already registered.")
        new_user = User(phone_number=serializer.validated_data["phone_number"])
        new_user.set_unusable_password()
        new_user.save()
        send_otp.delay(new_user.phone_number, "123456")
        return APIResponse.success(
            data={"phone_number": new_user.phone_number},
            message="OTP sent successfully.",
        )
    return APIResponse.error(message="Invalid data.", errors=serializer.errors)
