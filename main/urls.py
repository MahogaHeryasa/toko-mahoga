from django.urls import path
from django.contrib.auth import views as auth_views # Import view bawaan Django
from . import views

urlpatterns = [
    path('', views.daftar_produk, name='daftar_produk'),
    
    # --- Sistem Autentikasi ---
    # Menggunakan Login bawaan Django, tapi UI-nya dari file login.html kita
    path('login/', auth_views.LoginView.as_view(
        template_name='main/login.html',
        next_page='/',
    ), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('account/', views.account_page, name='account'),
    path('account/edit/', views.edit_account, name='edit_account'),
    path('ulasan/<int:produk_id>/', views.tambah_ulasan, name='tambah_ulasan'),
]