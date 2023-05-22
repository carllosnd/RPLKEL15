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
    statuspembayaran = models.CharField(max_length=1,null=True)
    idproduk = models.ForeignKey(UserProduct, on_delete=models.CASCADE)
    
class Transaksi(models.Model):
    idpembayaran = models.CharField(primary_key=True, max_length=4)
    nama = models.CharField(max_length=255)
    alamat = models.CharField(max_length=255)
    tglpembayaran = models.DateField()
    totalpembayaran = models.IntegerField()
    metodepembayaran = models.CharField(max_length=255)

class Penjualan(models.Model):
    idproduk = models.ForeignKey(UserProduct, on_delete=models.CASCADE)
    hargajual = models.DecimalField(max_digits=15, decimal_places=2)
    stok = models.IntegerField(default=0)
    total_terjual = models.IntegerField(default=0)

class Notifikasi(models.Model):
    idnotifikasi = models.AutoField(primary_key=True)
    pesannotifikasi = models.CharField(max_length=225)
    statusnotifikasi = models.CharField(max_length=1)
    
