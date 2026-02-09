import json

from django.conf import settings
from google import genai

import json

from django.conf import settings
from google import genai
from google.genai import types

from .schema import FoodAnalysisResponse


def get_food_analysis(image):

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=[image],
        config=types.GenerateContentConfig(
            system_instruction="Ты — профессиональный эксперт-нутрициолог...",
            response_mime_type="application/json",
            response_schema=FoodAnalysisResponse,
            temperature=0.1,
        ),
    )
    return json.loads(response.text)
