from django.urls import path
from . import views

urlpatterns = [
    # Menangkap angka ID dari URL (misal: /produk/1/)
    path('<int:id>/', views.detail_produk, name='detail_produk'), 
]