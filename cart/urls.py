from django.urls import path
from . import views

urlpatterns = [
    path('', views.halaman_cart, name='halaman_cart'),
    path('tambah/<int:produk_id>/', views.tambah_ke_cart, name='tambah_ke_cart'),
    path('update/<int:item_id>/<str:action>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.proses_checkout, name='proses_checkout'),
    path('checkout-langsung/<int:produk_id>/', views.checkout_langsung, name='checkout_langsung'),
    path('pembayaran/<str:order_id>/', views.halaman_pembayaran, name='halaman_pembayaran'),
    path('cek-status/<str:order_id>/', views.cek_status_pesanan, name='cek_status_pesanan'),
    path('pembayaran-berhasil/<str:order_id>/', views.pembayaran_berhasil, name='pembayaran_berhasil'),
    path('isi-alamat/<str:order_id>/', views.isi_alamat, name='isi_alamat'),
    path('simpan-alamat/<str:order_id>/', views.simpan_alamat, name='simpan_alamat'),
    path('tracking/', views.tracking_order, name='tracking_order'),
]