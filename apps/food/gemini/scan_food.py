import json
from collections import OrderedDict

import PIL.Image
from django.conf import settings
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import FoodAnalysisSerializer
from .services import get_food_analysis


class ImageAnalyzeView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get("image")
        if not file:
            return Response({"error": "No image provided"}, status=400)
        img = PIL.Image.open(file)
        try:
            result_data = get_food_analysis(img)
        except Exception as e:
            return Response({"error": f"AI analysis failed: {str(e)}"}, status=500)

        serializer = FoodAnalysisSerializer(data=result_data)
        if serializer.is_valid():
            return Response(serializer.data)
