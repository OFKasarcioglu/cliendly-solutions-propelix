from unfold.admin import ModelAdmin, TabularInline
from django.contrib import admin
from .models import StokHareket, StokHareketKalemi, StokLog


class StokHareketKalemiInline(TabularInline):
    model = StokHareketKalemi
    extra = 1
    fields = ["urun", "miktar"]
    classes = ["collapse"]  # istersen kaldır


@admin.register(StokHareket)
class StokHareketAdmin(ModelAdmin):
    list_display = ("hareket_turu", "referans_no", "olusturan", "olusturma_tarihi")
    list_filter = ("hareket_turu", "olusturma_tarihi")
    search_fields = ("referans_no", "aciklama")
    inlines = [StokHareketKalemiInline]

    def save_model(self, request, obj, form, change):
        if not obj.olusturan:
            obj.olusturan = request.user
        super().save_model(request, obj, form, change)


@admin.register(StokLog)
class StokLogAdmin(ModelAdmin):
    list_display = ("urun", "hareket_turu", "miktar", "olusturan", "olusturma_tarihi")
    list_filter = ("hareket_turu", "olusturma_tarihi", "olusturan")
    search_fields = ("urun__name", "urun__sku", "urun__barcode")
