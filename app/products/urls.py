from django.urls import include, path
from rest_framework.routers import DefaultRouter
from products.views.category import product_category_view
from products.views.products import search_products

urlpatterns = [
    path(
        "category/<int:category_id>/products/",
        product_category_view,
        name="category-products",
    ),
    path("products/search/", search_products, name="product-search"),
]
