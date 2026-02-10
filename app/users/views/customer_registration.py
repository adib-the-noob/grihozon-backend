from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view

from config.responses import APIResponse
from ..serializers.user_registration import (
    UserRegistrationOTPRequest,
    UserRegistrationSerializer,
)
from ..jwt import get_access_token, get_refresh_token
from ..tasks.otp_service import send_otp
from ..models.otp import OTP
from ..jwt import get_access_token

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
        with transaction.atomic():
            new_user = User(phone_number=serializer.validated_data["phone_number"])
            new_user.set_unusable_password()
            new_user.save()
            otp = OTP.objects.create(user=new_user, code="123456")
        send_otp.delay(new_user.phone_number, otp.code)
        return APIResponse.success(
            data={"phone_number": new_user.phone_number},
            message="OTP sent successfully.",
        )
    return APIResponse.error(message="Invalid data.", errors=serializer.errors)


@api_view(["POST"])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        otp = OTP.objects.filter(
            user__phone_number=serializer.validated_data["phone_number"],
            code=serializer.validated_data["otp"],
            is_used=False,
        ).first()
        if not otp:
            return APIResponse.error(message="Invalid or used OTP.")
        with transaction.atomic():
            user = otp.user
            user.is_verified = True
            user.save()
            otp.is_used = True
            otp.save()
        return APIResponse.success(
            data={
                "user_id": user.id,
                "phone_number": user.phone_number,
                "tokens": {
                    "access": get_access_token(user),
                    "refresh": get_refresh_token(user),
                },
            },
            message="User registered successfully.",
        )
    return APIResponse.error(message="Invalid data.", errors=serializer.errors)


@api_view(["POST"])
def login_otp_request(request):
    serializer = UserRegistrationOTPRequest(data=request.data)
    if serializer.is_valid():
        user = User.objects.filter(
            phone_number=serializer.validated_data["phone_number"],
            is_verified=True,
        ).first()
        if not user:
            return APIResponse.error(message="User not found or not verified.")
        otp = OTP.objects.create(user=user, code="123456")
        send_otp.delay(user.phone_number, otp.code)
        return APIResponse.success(
            data={"phone_number": user.phone_number},
            message="OTP sent successfully.",
        )
    return APIResponse.error(message="Invalid data.", errors=serializer.errors)

@api_view(["POST"])
def verify_login_otp(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        otp = OTP.objects.filter(
            user__phone_number=serializer.validated_data["phone_number"],
            code=serializer.validated_data["otp"],
            is_used=False,
        ).first()
        if not otp:
            return APIResponse.error(message="Invalid or used OTP.")
        with transaction.atomic():
            user = otp.user
            otp.is_used = True
            otp.save()
        return APIResponse.success(
            data={
                "user_id": user.id,
                "phone_number": user.phone_number,
                "tokens": {
                    "access": get_access_token(user),
                    "refresh": get_refresh_token(user),
                },
            },
            message="Login successful.",
        )
    return APIResponse.error(message="Invalid data.", errors=serializer.errors)

@api_view(["POST"])
def me(request):
    user = request.user
    if not user.is_authenticated:
        return APIResponse.error(message="Authentication required.")
    return APIResponse.success(
        data={
            "user_id": user.id,
            "phone_number": user.phone_number,
            "user_role": user.user_role,
            "is_verified": user.is_verified,
        },
        message="User details retrieved successfully.",
    )
