from django.urls import path
from .views import index, tambah_product, postproduct, dataproduct, updateproduct, postupdate_product, delete_product, welcome, tentang, pemesanan, tambah_pemesanan, postpemesanan

urlpatterns = [
    path('', index, name="home"),
    path('tambah_product', tambah_product, name="tambah_product"),
    path('post_product', postproduct, name="postproduct"),
    path('data_product', dataproduct, name="dataproduct"),
    path('update_product/<str:idproduk>', updateproduct, name="updateproduct"),
    path('postupdate_product', postupdate_product, name="postupdateproduct"),
    path('delete_product/<str:idproduk>', delete_product, name="deleteproduct"),
    path('welcome', welcome, name='welcome'),
    path('tentang', tentang, name='tentang'),
    path('pemesanan', pemesanan, name='pemesanan'),
    path('tambah_pemesanan', tambah_pemesanan, name='tambahpemesanan'),
    path('post_pemesanan', postpemesanan, name='postpemesanan'),
]