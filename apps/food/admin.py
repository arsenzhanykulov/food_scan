from django.contrib import admin
from django.utils.html import format_html

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("show_image", "name", "category", "colored_score", "created_at")
    search_fields = ("name", "category", "summary_note")
    list_filter = ("category", "created_at")
    ordering = ("-created_at",)

    def show_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 5px;" />',
                obj.image.url,
            )
        return "Нет фото"

    show_image.short_description = "Фото"

    def colored_score(self, obj):
        score = obj.health_score if obj.health_score is not None else 0.0

        if score >= 8.0:
            color = "#28a745"  # Зеленый
        elif score >= 5.0:
            color = "#ffc107"  # Желтый
        else:
            color = "#dc3545"  # Красный

        return format_html(
            '<b style="color: {}; font-size: 1.1em;">{}</b>', color, f"{score:.1f}"
        )

    colored_score.short_description = "Рейтинг"
