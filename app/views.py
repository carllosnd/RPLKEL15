import datetime
from multiprocessing import context
import os
import time
from django.db import connection
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse

from .models import Pemesanan, Penjualan, UserProduct
from django.contrib import messages
import json

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout


def index(request):
    return render(request, 'layout/index.html')


def produk(request):
    produk = UserProduct.objects.all()
    context = {
        'produk': produk
    }
    return render(request, 'user/produk.html', context)


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
        messages.success(request, 'data product berhasil disimpan')
    return redirect('/data_product')


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

    product = UserProduct.objects.get(idproduk=idmakanan)

    if Pemesanan.objects.filter(idpemesanan=idpemesanan).exists():
        messages.error(request, 'id pemesanan sudah ada')
        return redirect('/tambah_pemesanan')
    else:
        tambah_pemesanan = Pemesanan(
            idpemesanan=idpemesanan,
            tglpemesanan=datetime.date.today(),
            jumlahpemesanan=jlhpemesanan,
            totalbayar=product.hargaproduct * int(jlhpemesanan),
            keterangan=keterangan,
            idproduk=product,
        )
        tambah_pemesanan.save()
        messages.success(request, 'data pesananan berhasil disimpan')
    return redirect('/pemesanan')


def pemesanan(request):

    view = Pemesanan.objects.all().order_by('-idpemesanan')
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


def postupdate_pesanan(request, idproduk):
    pesanan = get_object_or_404(Pemesanan, pk=idproduk)
    

    if request.method == 'POST':
        pesanan.idpemesanan = request.POST.get('idpemesanan')
        pesanan.jlhpemesanan = request.POST.get('jlhpemesanan')
        pesanan.totalbayar = int(request.POST['jlhpemesanan']) * pesanan.idproduk.hargaproduct
        pesanan.keterangan = pesanan.request.get('keterangan')
        idproduk
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
            return redirect('/data_product')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('/welcome')

def penjualan(request):
    daftar_penjualan = Penjualan.objects.all()
    context = {
        'daftar_penjualan': daftar_penjualan
    }
    return render(request, 'penjualan/penjualan.html', context)

def save(self, *args, **kwargs):
        self.hargajual = self.idproduk.hargaproduct
        self.stok_terjual = self.pemesanan.jumlahpemesanan
        self.total_terjual = self.stok_terjual * self.hargajual
        super(Penjualan, self).save(*args, **kwargs)
