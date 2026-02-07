from django.urls import path

from .gemini.scan_food import ImageAnalyzeView

urlpatterns = [
    path("analyze/", ImageAnalyzeView.as_view(), name="analyze_image"),
]
