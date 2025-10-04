from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import Product


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = (
        "thumbnail",
        "name",
        "sku",
        "category",
        "brand",
        "unit_cost",
        "stock_quantity",     # ✅ güncel stok miktarı
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "category", "brand", "unit_type")
    search_fields = ("name", "sku", "barcode")

    fieldsets = (
        ("Temel Bilgiler", {
            "fields": ("name", "barcode", "sku", "description", "image", "preview")
        }),
        ("Stok & Maliyet", {
            "fields": ("stock_quantity", "unit_type", "unit_cost", "critical_stock_level")
        }),
        ("Sınıflandırma & Lojistik", {
            "fields": ("category", "brand", "warehouse_location")
        }),
        ("Durum", {
            "fields": ("is_active",)
        }),
    )

    readonly_fields = ("preview", "stock_quantity")  # stok admin'den değiştirilemez

    # ✅ Liste görünümünde küçük görsel
    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit:cover;border-radius:6px;box-shadow:0 0 4px rgba(0,0,0,0.3);" />',
                obj.image.url
            )
        return "-"
    thumbnail.short_description = "Görsel"

    # ✅ Detay sayfasında büyük önizleme
    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="150" height="150" style="object-fit:cover;border-radius:10px;box-shadow:0 0 6px rgba(0,0,0,0.4);" />',
                obj.image.url
            )
        return "-"
    preview.short_description = "Önizleme"
