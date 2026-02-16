import json

from django.conf import settings
from openai import OpenAI
from io import BytesIO

import base64

from .prompt import SYSTEM_PROMPT, USER_PROMPT

sys_prompt = SYSTEM_PROMPT


def get_food_analysis(img, error_context=None):

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    user_prompt = USER_PROMPT

    if error_context:
        user_prompt += (
            f"\n\nCRITICAL: Your previous response failed validation with errors: {error_context}. "
            f"You MUST fix these errors and follow the exact schema structure. Do not deviate."
        )

    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()
    base64_image = base64.b64encode(img_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4.1",
        temperature=0.1,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "food_analysis_response",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "maxLength": 60},
                        "category": {"type": "string", "maxLength": 60},
                        "health_score": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 100,
                        },
                        "summary_note": {"type": "string", "maxLength": 255},
                        "analysis_data": {
                            "type": "object",
                            "properties": {
                                "rating": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "number",
                                            "minimum": 0,
                                            "maximum": 10,
                                        },
                                        "color": {
                                            "type": "string",
                                            "enum": [
                                                "red",
                                                "yellow",
                                                "green",
                                                "orange",
                                            ],
                                        },
                                    },
                                    "required": ["value", "color"],
                                    "additionalProperties": False,
                                },
                                "should_eat": {
                                    "type": "object",
                                    "properties": {
                                        "verdict": {
                                            "type": "string",
                                            "enum": [
                                                "Excellent choice",
                                                "Good choice",
                                                "Not recommended",
                                                "Avoid",
                                            ],
                                        }
                                    },
                                    "required": ["verdict"],
                                    "additionalProperties": False,
                                },
                                "why_this_score": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "text": {
                                                "type": "string",
                                                "maxLength": 150,
                                            },
                                            "color": {
                                                "type": "string",
                                                "enum": [
                                                    "red",
                                                    "yellow",
                                                    "green",
                                                    "orange",
                                                ],
                                            },
                                        },
                                        "required": ["text", "color"],
                                        "additionalProperties": False,
                                    },
                                },
                                "nutrition": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "label": {
                                                "type": "string",
                                                "maxLength": 100,
                                            },
                                            "value": {
                                                "type": "string",
                                                "maxLength": 100,
                                            },
                                            "status": {
                                                "type": "string",
                                                "enum": ["good", "bad", "neutral"],
                                            },
                                        },
                                        "required": ["label", "value", "status"],
                                        "additionalProperties": False,
                                    },
                                },
                                "ingredients": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {
                                                "type": "string",
                                                "maxLength": 100,
                                            },
                                            "description": {
                                                "type": "string",
                                                "maxLength": 150,
                                            },
                                            "color": {
                                                "type": "string",
                                                "enum": [
                                                    "red",
                                                    "yellow",
                                                    "green",
                                                    "orange",
                                                ],
                                            },
                                        },
                                        "required": ["name", "description", "color"],
                                        "additionalProperties": False,
                                    },
                                },
                                "recommendation": {"type": "string", "maxLength": 255},
                            },
                            "required": [
                                "rating",
                                "should_eat",
                                "why_this_score",
                                "nutrition",
                                "ingredients",
                                "recommendation",
                            ],
                            "additionalProperties": False,
                        },
                    },
                    "required": [
                        "name",
                        "category",
                        "health_score",
                        "summary_note",
                        "analysis_data",
                    ],
                    "additionalProperties": False,
                },
            },
        },
    )

    raw = response.choices[0].message.content
    return json.loads(raw)
