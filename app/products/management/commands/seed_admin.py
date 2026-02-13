from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):
    help = "Create a default admin user"

    def handle(self, *args, **options):
        phone_number = "+8801700000000"
        username = "admin"
        email = "admin@grihozon.local"
        password = "admin123"

        # Check if admin user already exists by phone_number
        if User.objects.filter(phone_number=phone_number).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"Admin user with phone '{phone_number}' already exists. Skipping."
                )
            )
            return

        try:
            admin_user = User.objects.create_superuser(
                phone_number=phone_number,
                username=username,
                email=email,
                password=password,
                user_role="admin",
                is_verified=True,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Admin user created successfully\n"
                    f"  Phone: {phone_number}\n"
                    f"  Username: {username}\n"
                    f"  Password: {password}\n"
                    f"  Email: {email}\n"
                    f"  Role: Admin"
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Failed to create admin user: {str(e)}")
            )
