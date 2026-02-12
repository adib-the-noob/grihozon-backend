import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    MANAGER = "manager", "Manager"
    MODERATOR = "moderator", "Moderator"
    CUSTOMER = "customer", "Customer"


class User(AbstractUser):
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=17, unique=True)
    user_role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER,
    )

    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]  # username is still required but not for login

    class Meta:
        indexes = [
            models.Index(fields=["user_role"]),
            models.Index(fields=["is_verified"]),
        ]

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = (
                f"user_{self.phone_number}"
                if self.phone_number
                else f"user_{uuid.uuid4().hex[:12]}"
            )
        super().save(*args, **kwargs)

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


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.country}"