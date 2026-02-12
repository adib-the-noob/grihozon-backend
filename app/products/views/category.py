from rest_framework.decorators import api_view
from config.responses import APIResponse
from products.models.products import Product
from ..serializers.product_serializers import ProductSerializer
from ..pagination import CategoryProductPagination


@api_view(["GET"])
def product_category_view(request, category_id):
    qs = (
        Product.objects.filter(category_id=category_id, is_active=True)
        .prefetch_related("variants", "media")
        .order_by("-created_at")
    )
    paginator = CategoryProductPagination()
    page = paginator.paginate_queryset(qs, request, view=None)
    serializer = ProductSerializer(page, many=True)
    return APIResponse.success(data=serializer.data, meta=paginator.get_meta())

