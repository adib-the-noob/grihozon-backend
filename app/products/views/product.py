from rest_framework import viewsets
from rest_framework.decorators import action
from config.responses import APIResponse
from products.models.products import Product
from products.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True).prefetch_related(
        "variants", "images"
    )
    serializer_class = ProductSerializer

    @action(detail=False, methods=["get"], url_path="home")
    def home_page(self, request):
        qs = self.get_queryset().order_by("-created_at")[:12]
        serializer = self.get_serializer(qs, many=True)
        return APIResponse.success(data=serializer.data)
    
    @action(detail=True, methods=["get"], url_path="details")
    def details_page(self, request, pk=None):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return APIResponse.success(data=serializer.data)