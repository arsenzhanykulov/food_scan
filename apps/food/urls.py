from django.urls import path

from apps.food.gemini.scan_food import ImageAnalyzeView

urlpatterns = [
    path("analyze/", ImageAnalyzeView.as_view(), name="analyze_image"),
]
