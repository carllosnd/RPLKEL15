from django.urls import path
from .views import index, tambah_product, postproduct, dataproduct, updateproduct, postupdate_product, delete_product

urlpatterns = [
    path('index', index, name="index"),
    path('tambah_product', tambah_product, name="tambah_product"),
    path('post_product', postproduct, name="postproduct"),
    path('data_product', dataproduct, name="dataproduct"),
    path('update_product/<str:idproduk>', updateproduct, name="updateproduct"),
    path('postupdate_product', postupdate_product, name="postupdateproduct"),
    path('delete_product/<str:idproduk>', delete_product, name="deleteproduct")
]