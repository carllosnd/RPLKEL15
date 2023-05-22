import datetime
from multiprocessing import context
import os
import time
from django.db import connection
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse

from .models import Pemesanan, Penjualan, Transaksi, UserProduct,Notifikasi
from django.contrib import messages
import json

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'layout/index.html')


def produk(request):
    produk = UserProduct.objects.all()
    context = {
        'produk': produk
    }
    return render(request, 'user/produk.html', context)

@login_required(login_url=index)
def tambah_product(request):

    return render(request, 'products/tambah-product.html')


def postproduct(request):
    idproduk = request.POST['idproduk']
    gambar = request.FILES['gambar']
    namaproduct = request.POST['namaproduct']
    hargaproduct = request.POST['hargaproduct']
    deskripsi = request.POST['deskripsi']
    stok = request.POST['stok']
    
    if UserProduct.objects.filter(idproduk=idproduk).exists():
        messages.error(request, 'id product sudah ada')
        return redirect('/tambah_product')
    else:
        tambah_product = UserProduct(
            idproduk=idproduk,
            gambar=gambar,
            namaproduct=namaproduct,
            hargaproduct=hargaproduct,
            deskripsi=deskripsi,
            stok=stok,
        )
        tambah_product.save()
        # insert penjualan
        product = UserProduct.objects.get(idproduk=idproduk)
        tambah_penjualan = Penjualan(
            idproduk=product,
            hargajual=product.hargaproduct,
            stok=int(product.stok),
        )
        tambah_penjualan.save()
        messages.success(request, 'data product berhasil disimpan')
    return redirect('/data_product')

@login_required(login_url=index)
def dataproduct(request):
    data_product = UserProduct.objects.all().order_by('-idproduk')
    context = {
        'data_product': data_product
    }
    return render(request, 'products/data-product.html', context)


def updateproduct(request, idproduk):
    data_product = UserProduct.objects.get(idproduk=idproduk)
    context = {
        'data_product': data_product
    }
    return render(request, 'products/update-product.html', context)


def postupdate_product(request):
    id = request.POST['idproduk']
    
    product = UserProduct.objects.get(idproduk=id)
    if len(request.FILES) != 0:
        if len(product.gambar) > 0:
            os.remove(product.gambar.path)
        product.gambar = request.FILES['gambar']
    product.namaproduct = request.POST.get('namaproduct')
    product.hargaproduct = request.POST.get('hargaproduct')
    product.deskripsi = request.POST.get('deskripsi')
    product.stok = request.POST.get('stok')
    product.save()
    # update penjualan
    penjualan = Penjualan.objects.get(idproduk=id)
    penjualan.hargajual = request.POST.get('hargaproduct')
    penjualan.stok = request.POST.get('stok')
    penjualan.save()
    messages.success(request, 'Data berhasil di ubah')
    return redirect('/data_product')


def delete_product(request, idproduk):
    product = UserProduct.objects.get(idproduk=idproduk).delete()
    messages.success(request, 'Berhasil hapus data produk')
    return redirect('/data_product')


def welcome(request):
    return render(request, 'layout/index.html')


def tambah_pemesanan(request):
    datamakanan = UserProduct.objects.all()
    context = {
        'datamakanan': datamakanan
    }
    return render(request, 'pemesanan/tambah-pesanan.html', context)


def postpemesanan(request):
    idpemesanan = request.POST['idpemesanan']
    jlhpemesanan = request.POST['jumlahpemesanan']
    keterangan = request.POST['keterangan']
    idmakanan = request.POST['idproduk']
    
    product = UserProduct.objects.get(idproduk = idmakanan)
    
    if Pemesanan.objects.filter(idpemesanan=idpemesanan).exists():
        messages.error(request, 'id pemesanan sudah ada')
        return redirect('/tambah_pemesanan')
    if int (product.stok) <= 0:
        messages.error(request, 'Stok makanan sudah habis')
        return redirect('/tambah_pemesanan')
    else:
        # insert pe = 'msanan
        tambah_pemesanan = Pemesanan(
            idpemesanan=idpemesanan,
            tglpemesanan=datetime.date.today(),
            jumlahpemesanan=jlhpemesanan,
            totalbayar= product.hargaproduct * int(jlhpemesanan),
            keterangan=keterangan,
            idproduk=product,
            statuspembayaran='B'
        )
        tambah_pemesanan.save()
        # update penjualan
        penjualan = Penjualan.objects.get(idproduk=idmakanan)
        penjualan.stok = penjualan.stok - int(jlhpemesanan)
        penjualan.total_terjual = penjualan.total_terjual + int(jlhpemesanan)
        penjualan.save()
        #update produk
        produk = UserProduct.objects.get(idproduk=idmakanan)
        produk.stok = str(int(produk.stok) - int(jlhpemesanan))
        produk.save()
        # buat notifikasi
        buat_notifikasi = Notifikasi(
            pesannotifikasi = 'Ada Pesanan Masuk',
            statusnotifikasi = 'B'
        )
        buat_notifikasi.save()
        messages.success(request, 'data pesananan berhasil disimpan')
    return redirect('/pemesanan')


def pemesanan(request):

    view = Pemesanan.objects.filter(statuspembayaran='B').order_by('-idpemesanan')
    context = {
        'view_pesanan': view
    }
    return render(request, 'pemesanan/pemesanan.html', context)


def updatepesanan(request, idpemesanan):
    data_pesanan = Pemesanan.objects.get(idpemesanan=idpemesanan)
    product = UserProduct.objects.all()
    context = {
        'data_pesanan': data_pesanan,
        'product': product
    }
    return render(request, 'pemesanan/update-pesanan.html', context)


def postupdate_pesanan(request):
    idpemesanan = request.POST['idpemesanan']
    jlhpemesanan = request.POST['jumlahpemesanan']
    keterangan = request.POST['keterangan']
    idproduk = request.POST['idproduk']
    
    product = UserProduct.objects.get(idproduk=idproduk)
    pesanan = Pemesanan.objects.get(idpemesanan=idpemesanan)
    # update penjualan
    penjualan = Penjualan.objects.get(idproduk=idproduk)
    penjualan.stok = penjualan.stok + pesanan.jumlahpemesanan - int(jlhpemesanan)
    penjualan.total_terjual = penjualan.total_terjual - pesanan.jumlahpemesanan + int(jlhpemesanan)
    penjualan.save()
    # insert pemesanan
    pesanan.tglpemesanan = datetime.date.today()
    pesanan.jumlahpemesanan = jlhpemesanan
    pesanan.totalbayar = int(jlhpemesanan) * product.hargaproduct
    pesanan.keterangan = keterangan
    pesanan.idproduk = product
    pesanan.save()
    messages.success(request, 'pesanan berhasil diubah')
    return redirect('/pemesanan')


def delete_pesanan(request, idpemesanan):
    pesanan = Pemesanan.objects.get(idpemesanan=idpemesanan).delete()
    messages.success(request, 'Berhasil hapus pesanan')
    return redirect('/pemesanan')


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('/penjualan')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('/welcome')

def penjualan(request):
    daftar_penjualan = Penjualan.objects.all()
    list_notifikasi = Notifikasi.objects.filter(statusnotifikasi='B')
    jumlah_notifikasi = '0'
    if list_notifikasi:
        jumlah_notifikasi = len(list_notifikasi)
    context = {
        'daftar_penjualan': daftar_penjualan,
        'list_notifikasi':list_notifikasi,
        'jumlah_notifikasi':jumlah_notifikasi
    }
    return render(request, 'penjualan/penjualan.html', context)

def save(self, *args, **kwargs):
        self.hargajual = self.idproduk.hargaproduct
        self.stok = self.pemesanan.jumlahpemesanan
        self.total_terjual = self.stok * self.hargajual
        super(Penjualan, self).save(*args, **kwargs)
        
def transaksi(request):
    datapesanan = Pemesanan.objects.filter(statuspembayaran='B').aggregate(total=Sum('totalbayar'))['total']
    context = {
        'datapesanan': datapesanan
    }
    return render(request, 'transaksi/tambah-transaksi.html', context)
        
def postpembayaran(request):
    idpembayaran = request.POST['idpembayaran']
    nama = request.POST['nama']
    alamat = request.POST['alamat']
    totalpembayaran = request.POST['totalpembayaran']
    metodepembayaran = request.POST['metodepembayaran']
    
    if Transaksi.objects.filter(idpembayaran=idpembayaran).exists():
        messages.error(request, 'id pembayaran sudah ada')
        return redirect('/transaksi')
    else:
        transaksi_pembayaran = Transaksi(
            idpembayaran = idpembayaran,
            nama = nama,
            alamat = alamat,
            tglpembayaran = datetime.date.today(),
            totalpembayaran = totalpembayaran,
            metodepembayaran = metodepembayaran,
        )
        # update pemesanan
        pemesanan = Pemesanan.objects.filter(statuspembayaran='B')
        for i in range(len(pemesanan)):
            pemesanan[i].statuspembayaran = 'S'
            pemesanan[i].save()
        transaksi_pembayaran.save()
        messages.success(request, 'pembayaran berhasil')
    return redirect("/pembayaran")

def pembayaran(request):
    view_transaksi = Transaksi.objects.all().order_by('-idpembayaran')
    context = {
        'view_transaksi': view_transaksi
    }
    return render(request, 'transaksi/data-transaksi.html', context)

def notifikasi_terbaca(request,idnotifikasi):
    notifikasi = Notifikasi.objects.get(idnotifikasi=idnotifikasi)
    notifikasi.statusnotifikasi = 'S'
    notifikasi.save()
    messages.success(request, 'Notifikasi Telah Terbaca')
    return redirect(request.META.get('HTTP_REFERER'))