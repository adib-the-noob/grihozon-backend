from django.db import models
from .brands import Brand, Manufacturer, Country
from .category import Category

class Product(models.Model):
    name = models.CharField(max_length=255)
    name_bd = models.CharField(max_length=255, blank=True)
    description = models.JSONField(default=dict, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.SET_NULL, null=True, blank=True
    )
    origin_country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True
    )
    type = models.ForeignKey(
        "ProductType", on_delete=models.SET_NULL, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.name


class ProductVariant(models.Model):

    DISCOUNT_PERCENT = "PERCENT"
    DISCOUNT_AMOUNT = "AMOUNT"
    DISCOUNT_TYPE_CHOICES = [
        (DISCOUNT_PERCENT, "Percent"),
        (DISCOUNT_AMOUNT, "Amount"),
    ]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    sku = models.CharField(max_length=100, unique=True)
    unit_value = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.ForeignKey("Unit", on_delete=models.SET_NULL, null=True, blank=True)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_type = models.CharField(
        max_length=10, choices=DISCOUNT_TYPE_CHOICES, null=True, blank=True
    )
    discount_value = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    stock_qty = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "product_variants"

    def __str__(self):
        return f"{self.product.name} - {self.sku}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image_url = models.TextField()
    sort_order = models.IntegerField(default=0)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.product.name} - Image {self.pk}"


class ProductType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=50, help_text="kg|gm|L|pcs")
    base_unit = models.CharField(max_length=50, null=True, blank=True)
    multiplier_to_base = models.DecimalField(
        max_digits=10, decimal_places=4, null=True, blank=True
    )

    def __str__(self):
        return self.name
