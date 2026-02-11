from typing import Literal

import typing_extensions as typing


class WhyThisScore(typing.TypedDict):
    text: str
    color: str  # red, yellow, green, orange


class Rating(typing.TypedDict):
    value: float  # 1.00 - 10.00
    color: str  # red, yellow, green, orange


class NutritionItem(typing.TypedDict):
    label: str  # Название: "Белки", "Сахар", "Витамин C"
    value: str  # Значение: "12г", "0.5г", "15% от суточной нормы"
    status: str  # Оценка: "good", "bad", "neutral"


class Ingredient(typing.TypedDict):
    name: str
    description: str
    color: str  # red, yellow, green, orange


class ShouldEat(typing.TypedDict):
    verdict: str
    verdict: Literal["Отличный выбор", "Хороший выбор", "Не рекомендуется", "Избегайте"]


class AnalyzeData(typing.TypedDict):
    rating: Rating
    should_eat: ShouldEat
    why_this_score: list[WhyThisScore]
    nutrition: list[NutritionItem]
    ingredients: list[Ingredient]
    recommendation: str


class FoodAnalysisResponse(typing.TypedDict):
    name: str
    category: str
    health_score: int
    summary_note: str
    analysis_data: AnalyzeData
