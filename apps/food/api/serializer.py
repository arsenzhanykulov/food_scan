from rest_framework import serializers
from ..models import Product


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "category",
            "health_score",
            "summary_note",
            "image",
            "created_at",
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("analysis_data",)
