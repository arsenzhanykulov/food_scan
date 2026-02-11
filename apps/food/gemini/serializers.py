from rest_framework import serializers


class AnalyzeDataSerializer(serializers.Serializer):
    rating = serializers.DictField()
    should_eat = serializers.DictField()
    why_this_score = serializers.ListField()
    nutrition = serializers.ListField()
    ingredients = serializers.ListField()
    recommendation = serializers.CharField()


class FoodAnalysisResponseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=60)
    category = serializers.CharField(max_length=60)
    health_score = serializers.IntegerField(min_value=0, max_value=100)
    summary_note = serializers.CharField(max_length=255)
    analyze_data = AnalyzeDataSerializer()
