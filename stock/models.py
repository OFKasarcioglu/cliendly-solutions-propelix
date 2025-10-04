from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product

User = get_user_model()


class StokHareket(models.Model):
    HAREKET_TURLERI = [
        ("IN", "Stok Girişi"),
        ("OUT", "Stok Çıkışı"),
    ]

    hareket_turu = models.CharField("Hareket Türü", max_length=3, choices=HAREKET_TURLERI)
    referans_no = models.CharField("Referans No", max_length=50, blank=True, null=True)
    aciklama = models.TextField("Açıklama", blank=True, null=True)
    olusturma_tarihi = models.DateTimeField("Oluşturma Tarihi", auto_now_add=True)
    olusturan = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="stok_hareketleri", verbose_name="Oluşturan"
    )

    class Meta:
        verbose_name = "Stok Hareketi"
        verbose_name_plural = "Stok Hareketleri"
        ordering = ["-olusturma_tarihi"]

    def __str__(self):
        return f"{self.get_hareket_turu_display()} - {self.olusturma_tarihi.strftime('%Y-%m-%d %H:%M')}"


class StokHareketKalemi(models.Model):
    hareket = models.ForeignKey(StokHareket, on_delete=models.CASCADE, related_name="kalemler", verbose_name="Hareket")
    urun = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Ürün")
    miktar = models.PositiveIntegerField("Miktar")

    class Meta:
        verbose_name = "Stok Hareket Kalemi"
        verbose_name_plural = "Stok Hareket Kalemleri"

    def __str__(self):
        return f"{self.urun.name} x {self.miktar}"

    def save(self, *args, **kwargs):
        # Güncelleme öncesi eski miktarı bul
        old_miktar = None
        if self.pk:
            old_miktar = StokHareketKalemi.objects.get(pk=self.pk).miktar

        super().save(*args, **kwargs)

        # Ürün stoğunu fark kadar güncelle
        fark = self.miktar - (old_miktar or 0)
        if fark != 0:
            if self.hareket.hareket_turu == "IN":
                self.urun.stock_quantity += fark
            elif self.hareket.hareket_turu == "OUT":
                self.urun.stock_quantity -= fark
            self.urun.save(update_fields=["stock_quantity"])

            # Log kaydı oluştur
            StokLog.objects.create(
                urun=self.urun,
                hareket=self.hareket,
                miktar=fark,
                hareket_turu=self.hareket.hareket_turu,
                olusturan=self.hareket.olusturan,
            )


class StokLog(models.Model):
    HAREKET_TURLERI = [
        ("IN", "Stok Girişi"),
        ("OUT", "Stok Çıkışı"),
    ]

    urun = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stok_loglari", verbose_name="Ürün")
    hareket = models.ForeignKey(StokHareket, on_delete=models.CASCADE, verbose_name="Hareket")
    miktar = models.IntegerField("Miktar")
    hareket_turu = models.CharField("Hareket Türü", max_length=3, choices=HAREKET_TURLERI)
    olusturan = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Oluşturan")
    olusturma_tarihi = models.DateTimeField("Oluşturma Tarihi", auto_now_add=True)

    class Meta:
        verbose_name = "Stok Log"
        verbose_name_plural = "Stok Logları"
        ordering = ["-olusturma_tarihi"]

    def __str__(self):
        return f"{self.urun.name} - {self.get_hareket_turu_display()} {self.miktar} ({self.olusturma_tarihi.strftime('%Y-%m-%d %H:%M')})"
