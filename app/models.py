from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProduct(models.Model):
    idproduk = models.CharField(primary_key=True, max_length=4)
    gambar = models.ImageField(upload_to='static/assets/dist/img', blank=True, null=True)
    namaproduct = models.CharField(max_length=255)
    hargaproduct = models.IntegerField()
    deskripsi = models.CharField(max_length=255)
    stok = models.CharField(max_length=6)
    
class Pemesanan(models.Model):
    idpemesanan = models.CharField(primary_key=True, max_length=4)
    tglpemesanan = models.DateField()
    jumlahpemesanan = models.IntegerField()
    totalbayar = models.IntegerField()
    keterangan = models.CharField(max_length=255)
    idproduk = models.ForeignKey(UserProduct, on_delete=models.CASCADE)

class Penjualan(models.Model):
    idproduk = models.ForeignKey(UserProduct, on_delete=models.CASCADE)
    idpemesanan = models.ForeignKey(Pemesanan, on_delete=models.CASCADE)
    hargajual = models.DecimalField(max_digits=15, decimal_places=2)
    stok_terjual = models.IntegerField(default=0)
    total_terjual = models.DecimalField(max_digits=15, decimal_places=2, default=0)
