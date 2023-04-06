from django.db import connection
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Pemesanan, UserProduct
from django.contrib import messages
import json


def index(request):
    context = {
        'name': 'carlos'
    }
    return render(request, 'home.html', context)


def tambah_product(request):
    
    return render(request, 'tambah-product.html')

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
    return render(request, 'data-product.html', context)

def updateproduct(request, idproduk):
    data_product = UserProduct.objects.get(idproduk=idproduk)
    context = {
        'data_product': data_product
    }
    return render(request, 'update-product.html', context)


def postupdate_product(request):
    id = request.POST['idproduk']
    gambar = request.FILES['gambar']
    namaproduct = request.POST['namaproduct']
    hargaproduct = request.POST['hargaproduct']
    deskripsi = request.POST['deskripsi']
    stok = request.POST['stok']
    
    product = UserProduct.objects.get(idproduk=id)
    product.gambar = gambar
    product.namaproduct = namaproduct
    product.hargaproduct = hargaproduct
    product.deskripsi = deskripsi
    product.stok = stok
    product.save()
    messages.success(request, 'Data berhasil di ubah')
    return redirect('/data_product')
    
def delete_product(request, idproduk):
    product = UserProduct.objects.get(idproduk=idproduk).delete()
    messages.success(request, 'Berhasil hapus data produk')
    return redirect('/data_product')

def welcome(request):
    return render(request, 'home.html')

def tentang(request):
    return render(request, 'tentang.html')

def tambah_pemesanan(request):
    datamakanan = UserProduct.objects.all()
    context = {
        'datamakanan': datamakanan
    }
    return render(request, 'tambah-pesanan.html', context)

def postpemesanan(request):
    idpemesanan = request.POST['idpemesanan']
    tanggalpemesanan = request.POST['tanggalpemesanan']
    jlhpemesanan = request.POST['jumlahpemesanan']
    keterangan = request.POST['keterangan']
    idmakanan = request.POST['idproduk']
    
    product = UserProduct.objects.get(idproduk = idmakanan)
    
    if Pemesanan.objects.filter(idpemesanan=idpemesanan).exists():
        messages.error(request, 'id pemesanan sudah ada')
        return redirect('/tambah_pemesanan')
    else:
        tambah_pemesanan = Pemesanan(
            idpemesanan=idpemesanan,
            tglpemesanan=tanggalpemesanan,
            jumlahpemesanan=jlhpemesanan,
            totalbayar=jlhpemesanan * product.hargaproduct,
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
    return render(request, 'pemesanan.html', context)