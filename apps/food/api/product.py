from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ..models import Product
from .serializer import ProductListSerializer, ProductDetailSerializer


class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.all(
            user=self.request.user,
        ).order_by("-created_at")

class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(
            user=self.request.user,
            is_active=True,
        )

class ProductActivateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        product = get_object_or_404(
            Product,
            pk=pk,
            user=request.user,
        )

        product.is_active = True
        product.save(update_fields=["is_active"])

        serializer = ProductListSerializer(product)

        return Response(serializer.data)