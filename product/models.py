from django.db import models
from inventory.models import Category, Brand
from django.utils.html import format_html

UNIT_CHOICES = [
    ("PCS", "Piece"),
    ("BOX", "Box"),
    ("PKG", "Package"),
    ("KG", "Kilogram"),
    ("G", "Gram"),
    ("TON", "Ton"),
    ("L", "Liter"),
    ("ML", "Milliliter"),
    ("SET", "Set"),
    ("PALLET", "Pallet"),
]


class Product(models.Model):
    # 1️⃣ Temel Bilgiler
    name = models.CharField("Product Name", max_length=150)
    barcode = models.CharField("Barcode", max_length=50, blank=True, null=True)
    sku = models.CharField("Stock Code", max_length=50, unique=True)
    description = models.TextField("Description", blank=True, null=True)
    image = models.ImageField("Image", upload_to="products/", blank=True, null=True)
    

    # 2️⃣ Stok ve Maliyet
    initial_quantity = models.PositiveIntegerField("Initial Quantity", default=0)
    unit_type = models.CharField("Unit Type", max_length=10, choices=UNIT_CHOICES, default="PCS")
    unit_cost = models.DecimalField("Unit Cost", max_digits=10, decimal_places=2, default=0)
    critical_stock_level = models.PositiveIntegerField("Critical Stock Level", default=0)

    # 3️⃣ Sınıflandırma ve Lojistik
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products", blank=True, null=True)
    stock_quantity = models.PositiveIntegerField("Stok Miktarı", default=0)
    warehouse_location = models.CharField("Warehouse Location", max_length=255, blank=True, null=True)

    # Ortak Alanlar
    is_active = models.BooleanField("Active", default=True)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    # 🔹 Görsel önizleme fonksiyonları
    def preview(self):
        if self.image:
            return format_html(
                '<img src="{}" width="200" height="200" style="object-fit:cover;border-radius:10px;box-shadow:0 0 8px #0003;" />',
                self.image.url,
            )
        return format_html(
            '<div style="width:200px;height:200px;display:flex;align-items:center;justify-content:center;'
            'background:#1e1e2f;color:#777;border-radius:10px;">No Image</div>'
        )
    preview.short_description = "Preview"

    def thumbnail(self):
        if self.image:
            return format_html(
                '<img src="{}" width="45" height="45" style="object-fit:cover;border-radius:6px;" />',
                self.image.url,
            )
        return "-"
    thumbnail.short_description = "Image"
