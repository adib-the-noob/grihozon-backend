from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    MANAGER = "manager", "Manager"
    MODERATOR = "moderator", "Moderator"
    CUSTOMER = "customer", "Customer"


class CustomUser(AbstractUser):
    email = models.EmailField(blank=True, null=True, help_text="Email address (optional)")
    phone_number = models.CharField(
        max_length=17,
        unique=True,
        help_text="Phone number (required)",
    )
    is_verified = models.BooleanField(default=False)
    user_role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]  # username is still required but not for login

    class Meta:
        indexes = [
            models.Index(fields=["phone_number"]),
            models.Index(fields=["user_role"]),
            models.Index(fields=["is_verified"]),
        ]

    def __str__(self):
        return f"{self.username} ({self.phone_number})"

    @property
    def is_admin(self):
        return self.user_role == UserRole.ADMIN

    @property
    def is_manager(self):
        return self.user_role == UserRole.MANAGER

    @property
    def is_moderator(self):
        return self.user_role == UserRole.MODERATOR

    @property
    def is_customer(self):
        return self.user_role == UserRole.CUSTOMER