from django.db import models
from django.contrib.auth import get_user_model
from products.models import ProductVariant

User = get_user_model()


class Cart(models.Model):
    """Shopping cart for users"""

    STATUS_ACTIVE = "ACTIVE"
    STATUS_CHECKED_OUT = "CHECKED_OUT"
    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_CHECKED_OUT, "Checked Out"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "carts"

    def __str__(self):
        return f"Cart {self.id} - {self.user.username}"


class CartItem(models.Model):
    """Items in shopping cart"""

    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items", db_column="cart_id"
    )
    variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, db_column="variant_id"
    )
    qty = models.IntegerField(default=1)
    price_at_add = models.DecimalField(max_digits=10, decimal_places=2)
    discount_at_add = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    class Meta:
        db_table = "cart_items"

    def __str__(self):
        return f"CartItem {self.id} - {self.variant.sku}"
