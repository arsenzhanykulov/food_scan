import json

from django.conf import settings
from google import genai
from google.genai import types

from .schema import FoodAnalysisResponse


def get_food_analysis(image, error_context=None):

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    prompt = "Проанализируй фото еды."
    system_instr = "Ты — нутрициолог. Верни JSON по схеме."

    if error_context:
        prompt += (
            f"\n\nВ твоем предыдущем ответе были ошибки валидации: {error_context}. "
            f"Пожалуйста, исправь их и строго следуй схеме."
        )
    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=[image],
        config=types.GenerateContentConfig(
            system_instruction=system_instr,
            response_mime_type="application/json",
            response_schema=FoodAnalysisResponse,
            temperature=0.1,
        ),
    )
    return json.loads(response.text)
