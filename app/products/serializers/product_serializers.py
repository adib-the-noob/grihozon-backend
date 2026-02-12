from rest_framework import serializers
from ..models.products import Product, ProductVariant, Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"


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
    media = MediaSerializer(many=True, read_only=True)

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
            "product_type",
            "is_active",
            "created_at",
            "updated_at",
            "variants",
            "media",
        ]


class ProductSearchSerializer(serializers.Serializer):
    q = serializers.CharField(required=False, allow_blank=True, max_length=255)
