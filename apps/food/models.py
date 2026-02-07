from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    category = models.CharField(max_length=255, blank=True, verbose_name="Категория")
    health_score = models.FloatField(verbose_name="Оценка")
    summary_note = models.CharField(
        max_length=255, blank=True, verbose_name="Краткий вердикт"
    )
    image = models.ImageField(upload_to="products/", verbose_name="Фото")
    analysis_data = models.JSONField(verbose_name="Полный JSON анализа")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.health_score}"
