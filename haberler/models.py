from django.db import models

# Create your models here.


class Gazeteci(models.Model):
    isim = models.TextField()
    soyisim = models.TextField()
    biyografi = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.isim} {self.soyisim}"


class Makale(models.Model):
    yazar = models.ForeignKey(
        Gazeteci, on_delete=models.CASCADE, related_name="makaleler"
    )
    baslik = models.TextField()
    aciklama = models.TextField()
    metin = models.TextField()
    sehir = models.TextField()
    yayinlanma_tarihi = models.DateField()
    aktif = models.BooleanField(default=True)
    yaratilma_tarihi = models.DateField(auto_now_add=True)
    güncellenme_tarihi = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.baslik
