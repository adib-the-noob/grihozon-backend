from django.db.models import Q
from rest_framework.decorators import api_view
from config.responses import APIResponse
from products.models.products import Product
from ..serializers.product_serializers import ProductSerializer, ProductSearchSerializer
from ..pagination import ProductPagination

@api_view(["GET"])
def search_products(request):
    params = ProductSearchSerializer(data=request.query_params)
    params.is_valid(raise_exception=True)
    query = params.validated_data.get("q", "")

    qs = (
        Product.objects.filter(is_active=True)
        .select_related(
            "brand",
            "category",
            "manufacturer",
            "origin_country",
            "product_type",
        )
        .prefetch_related("variants", "media")
    )

    if query:
        qs = qs.filter(
            Q(name__icontains=query)
            | Q(name_bd__icontains=query)
            | Q(brand__name__icontains=query)
            | Q(category__name__icontains=query)
            | Q(manufacturer__name__icontains=query)
            | Q(origin_country__name__icontains=query)
            | Q(product_type__name__icontains=query)
            | Q(variants__sku__icontains=query)
        )

    qs = qs.order_by("-created_at").distinct()
    paginator = ProductPagination()
    page = paginator.paginate_queryset(qs, request, view=None)
    serializer = ProductSerializer(page, many=True)
    return APIResponse.success(data=serializer.data, meta=paginator.get_meta())