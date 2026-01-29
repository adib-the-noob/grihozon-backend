from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    MANAGER = "manager", "Manager"
    MODERATOR = "moderator", "Moderator"
    CUSTOMER = "customer", "Customer"


class CustomUser(AbstractUser):
    """
    Custom User model extending AbstractUser with additional fields
    """

    # Override email to make it nullable
    email = models.EmailField(
        blank=True, null=True, help_text="Email address (optional)"
    )

    # Phone number field (mandatory)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        unique=True,
        help_text="Phone number (required)",
    )

    # Verification status
    is_verified = models.BooleanField(
        default=False,
        help_text="Designates whether this user has verified their phone number.",
    )

    # User role
    user_role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER,
        help_text="Role of the user in the system",
    )

    # Additional fields for better user management
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Use phone number as the unique identifier for login
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]  # username is still required but not for login

    class Meta:
        db_table = "users_customuser"
        verbose_name = "User"
        verbose_name_plural = "Users"
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

    def save(self, *args, **kwargs):
        # Ensure phone number is properly formatted
        if self.phone_number and not self.phone_number.startswith("+"):
            # Add default country code if not present
            if not self.phone_number.startswith("0"):
                self.phone_number = (
                    "+880" + self.phone_number
                )  # Bangladesh country code
            else:
                self.phone_number = (
                    "+880" + self.phone_number[1:]
                )  # Remove leading 0 and add country code

        super().save(*args, **kwargs)
