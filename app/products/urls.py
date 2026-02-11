from django.urls import include, path
from rest_framework.routers import DefaultRouter
from products.views.category import ProductCategoryView

urlpatterns = [
    path("category/<int:category_id>/products/", ProductCategoryView.as_view(), name="category-products"),
]
