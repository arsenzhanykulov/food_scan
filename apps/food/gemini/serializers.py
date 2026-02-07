from rest_framework import serializers


class FoodAnalysisSerializer(serializers.Serializer):
    name = serializers.CharField()
    rating = serializers.DictField()
    summary_note = serializers.CharField()
    should_eat = serializers.DictField()
    why_this_score = serializers.ListField()
    nutrition = serializers.ListField()
    ingredients = serializers.ListField()
    recommendation = serializers.CharField()
