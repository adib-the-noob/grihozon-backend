from django.contrib import admin
from .models.brands import Brand, Manufacturer, Country
from .models.category import Category
from .models.products import Product, ProductVariant, ProductImage, ProductType


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "category",
        "manufacturer",
        "is_active",
        "created_at",
    )
    search_fields = ("name", "brand__name", "category__name", "manufacturer__name")
    list_filter = ("is_active", "brand", "category", "manufacturer")
    ordering = ("-created_at",)


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("sku", "product", "mrp", "selling_price", "stock_qty", "is_active")
    search_fields = ("sku", "product__name")
    list_filter = (
        "is_active",
        "product__brand",
        "product__category",
        "product__manufacturer",
    )
    ordering = ("-id",)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image_url", "is_primary", "sort_order")
    search_fields = ("product__name",)
    list_filter = ("is_primary",)
    ordering = ("product", "sort_order")


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    search_fields = ("name", "parent__name")
    ordering = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
