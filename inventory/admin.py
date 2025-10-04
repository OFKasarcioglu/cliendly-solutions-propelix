from unfold.admin import ModelAdmin  # Unfold için özel admin
from django.contrib import admin
from .models import Category, Brand


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("name", "parent", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("parent__name", "name")


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ("name", "category", "parent", "is_active", "created_at")
    list_filter = ("is_active", "category")
    search_fields = ("name",)
    ordering = ("category__name", "parent__name", "name")
