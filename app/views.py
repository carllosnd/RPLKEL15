from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserProduct
from django.contrib import messages
import json


def index(request):
    context = {
        'name': 'carlos'
    }
    return render(request, 'index.html', context)

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
    
    # print(idproduk)
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