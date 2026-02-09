import PIL.Image
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from .serializers import FoodAnalysisSerializer
from .services import get_food_analysis


@extend_schema(
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "image": {
                    "description": "Изображение для анализа (JPG, PNG, JPEG)",
                }
            },
        }
    },
    description="Загрузите фото еды для анализа питания",
    summary="Анализ изображения с едой",
)
class ImageAnalyzeView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

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
