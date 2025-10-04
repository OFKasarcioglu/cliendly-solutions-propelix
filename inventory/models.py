from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["parent__name", "name"]

    def __str__(self):
        # Parent varsa parent > child mantığıyla göster
        if self.parent:
            return f"{self.parent} > {self.name}"
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="brands"
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="sub_brands",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ["category__name", "parent__name", "name"]

    def __str__(self):
        # Parent varsa parent > child mantığıyla göster
        if self.parent:
            return f"{self.parent} > {self.name}"
        return self.name
