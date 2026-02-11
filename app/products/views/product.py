from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from config.responses import APIResponse
from products.models.products import Product
from ..serializers.product_serializers import ProductSerializer
from ..pagination import CategoryProductPagination

class ProductCategoryView(APIView):
    pagination_class = CategoryProductPagination

    def get(self, request, category_id):
        qs = (
            Product.objects.filter(category_id=category_id, is_active=True)
            .prefetch_related("variants", "media")
            .order_by("-created_at")
        )
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request, view=self)
        serializer = ProductSerializer(page, many=True)
        return APIResponse.success(data=serializer.data, meta=paginator.get_meta())

