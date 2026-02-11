from rest_framework import serializers
from ..models.products import Product, ProductVariant, Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ["id", "image_url", "sort_order", "is_primary"]


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "sku",
            "unit_value",
            "unit",
            "mrp",
            "selling_price",
            "discount_type",
            "discount_value",
            "stock_qty",
            "is_active",
        ]


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "name_bd",
            "description",
            "brand",
            "category",
            "manufacturer",
            "origin_country",
            "type",
            "is_active",
            "created_at",
            "updated_at",
            "variants",
            "images",
        ]
