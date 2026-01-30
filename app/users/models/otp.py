from django.db import models
from django.utils import timezone
from datetime import timedelta
from ..models.user import CustomUser

OTP_EXPIRATION_MINUTES = 5


def get_otp_expiration():
    return timezone.now() + timedelta(minutes=OTP_EXPIRATION_MINUTES)

class OTPManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(expires_at__lt=timezone.now()).delete()
        return super().get_queryset().filter(expires_at__gte=timezone.now())

    def create_otp(self, user, code):
        self.filter(user=user).delete()
        return self.create(user=user, code=code)

class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=6, help_text="OTP Code")

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_otp_expiration)

    objects = OTPManager()

    class Meta:
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"

    def __str__(self):
        return f"OTP for {self.user.phone_number} - Code: {self.code}"

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    def is_valid(self, code):
        if self.is_expired:
            self.delete()
            return False
        return self.code == code
