import json

from django.conf import settings
from google import genai

from .schema import FoodAnalysisResponse


def get_food_analysis(image):

    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel(
        model_name="models/gemini-2.5-flash",
        system_instruction="Ты — профессиональный эксперт-нутрициолог... (весь наш текст про штрафы и категории",
    )

    response = model.generate_content(
        [image],
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": FoodAnalysisResponse,
            "temperature": 0.1,
        },
    )
    print(response.text)
    return json.loads(response.text)
