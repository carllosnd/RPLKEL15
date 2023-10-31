from django.urls import path
from .views import index, tambah_product, postproduct, dataproduct, updateproduct, postupdate_product, delete_product 
from .views import welcome, pemesanan, tambah_pemesanan, postpemesanan, updatepesanan, postupdate_pesanan, delete_pesanan, produk
from .views import login, logout, penjualan, pembayaran, postpembayaran,transaksi,notifikasi_terbaca,tandai_semua_terbaca, datacustomer
from .views import export_pdf_penjualan, export_pdf_transaksi, export_pdf_customer


urlpatterns = [
    path('', index, name="home"),
    path('tambah_product', tambah_product, name="tambah_product"),
    path('post_product', postproduct, name="postproduct"),
    path('data_product', dataproduct, name="dataproduct"),
    path('update_product/<str:idproduk>', updateproduct, name="updateproduct"),
    path('postupdate_product', postupdate_product, name="postupdateproduct"),
    path('delete_product/<str:idproduk>', delete_product, name="deleteproduct"),
    path('welcome', welcome, name='welcome'),
    path('pemesanan', pemesanan, name='pemesanan'),
    path('tambah_pemesanan/<str:idproduk>', tambah_pemesanan, name='tambahpemesanan'),
    path('post_pemesanan', postpemesanan, name='postpemesanan'),
    path('update_pesanan/<str:idpemesanan>', updatepesanan, name="updatepesanan"),
    path('postupdate_pesanan', postupdate_pesanan, name="postupdatepesanan"),
    path('delete_pesanan/<str:idpemesanan>', delete_pesanan, name="deletepesanan"),
    path('produk', produk, name="produk"),
    path("login/", login, name="login"),
    path("logout", logout, name="logout"),
    path('penjualan',penjualan,name='penjualan'),
    path('export-pdf-penjualan',export_pdf_penjualan, name='export_pdf_penjualan'),
    path('pembayaran',pembayaran,name='pembayaran'),
    path('postpembayaran',postpembayaran,name='postpembayaran'),
    path('transaksi',transaksi,name='transaksi'),
    path('export-pdf-transaksi', export_pdf_transaksi, name='export_pdf_transaksi'),
    path('notifikasi_terbaca/<str:idnotifikasi>',notifikasi_terbaca,name='notifikasi_terbaca'),
    path('datacustomer',datacustomer,name='datacustomer'),
    path('export-pdf-customer/',export_pdf_customer,name='export_pdf_customer'),
    path('tandai_semua_terbaca', tandai_semua_terbaca, name='tandaisemuaterbaca')

    
]