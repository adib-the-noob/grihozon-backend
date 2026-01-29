from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("phone_number", "username", "email")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("phone_number", "username", "email", "user_role", "is_verified")


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = (
        "username",
        "phone_number",
        "email",
        "user_role",
        "is_verified",
        "is_active",
        "date_joined",
    )
    list_filter = ("user_role", "is_verified", "is_active", "is_staff", "date_joined")
    search_fields = ("username", "phone_number", "email")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("phone_number", "email", "first_name", "last_name")},
        ),
        ("Status", {"fields": ("user_role", "is_verified")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "user_role",
                ),
            },
        ),
    )
