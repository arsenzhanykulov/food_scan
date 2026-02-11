import PIL.Image
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from .serializers import FoodAnalysisResponseSerializer
from .services import get_food_analysis
from ..models import Product
from apps.user.models import User


@extend_schema(
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "image": {
                    "type": "string",
                    "format": "binary",
                    "description": "Изображение для анализа (JPG, PNG, JPEG)",
                }
            },
            "required": ["image"],
        }
    },
    description="Загрузите фото еды для анализа питания",
    summary="Анализ изображения с едой",
)
class ImageAnalyzeView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("image")
        img = PIL.Image.open(file)

        max_retries = 2
        error_to_send = None

        for attempt in range(max_retries):
            try:
                result_data = get_food_analysis(img, error_context=error_to_send)

                serializer = FoodAnalysisResponseSerializer(data=result_data)

                if serializer.is_valid():
                    Product.objects.create(
                        user=request.user,
                        name=result_data["name"],
                        category=result_data.get("category", ""),
                        health_score=result_data["health_score"],
                        summary_note=result_data.get("summary_note", ""),
                        image=file,
                        analysis_data=result_data,
                        is_active=False,
                    )

                    return Response(serializer.data)

                error_to_send = str(serializer.errors)
                print(f"Попытка {attempt + 1} провалена. Ошибки: {error_to_send}")

            except Exception as e:
                return Response({"error": f"AI error: {str(e)}"}, status=500)

        return Response(
            {
                "error": "Не удалось получить валидный JSON после исправлений",
                "details": error_to_send,
            },
            status=400,
        )
