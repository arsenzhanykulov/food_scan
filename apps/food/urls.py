from django.urls import path

from apps.food.gemini.scan_food import ImageAnalyzeView
from apps.food.api.product import (
    ProductListView,
    ProductDetailView,
    ProductActivateView,
)

urlpatterns = [
    path("analyze/", ImageAnalyzeView.as_view(), name="analyze_image"),
    path("products/", ProductListView.as_view()),
    path("products/<int:pk>/", ProductDetailView.as_view()),
    path("products/<int:pk>/activate/", ProductActivateView.as_view()),
]
