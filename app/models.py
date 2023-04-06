from django.db import models

class UserProduct(models.Model):
    idproduk = models.CharField(primary_key=True, max_length=4)
    gambar = models.ImageField(upload_to='static/assets/dist/img', blank=True, null=True)
    namaproduct = models.CharField(max_length=255)
    hargaproduct = models.IntegerField()
    deskripsi = models.CharField(max_length=255)
    stok = models.CharField(max_length=6)
