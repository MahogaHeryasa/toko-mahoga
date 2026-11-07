from django.contrib import admin
from .models import Produk, GambarProduk, Kategori, Ulasan

# --- TAMBAHKAN KODE INI ---
class KategoriAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nama',)}

class GambarProdukInline(admin.TabularInline):
    model = GambarProduk
    extra = 3

class ProdukAdmin(admin.ModelAdmin):
    inlines = [GambarProdukInline]

admin.site.register(Kategori, KategoriAdmin) # Daftarkan kategori
admin.site.register(Produk, ProdukAdmin)

# Tambahkan konfigurasi untuk Ulasan
class UlasanAdmin(admin.ModelAdmin):
    # Menampilkan kolom-kolom ini di daftar tabel admin
    list_display = ('user', 'produk', 'rating', 'tanggal')
    
    # Menambahkan fitur filter di sebelah kanan
    list_filter = ('rating', 'tanggal', 'produk')
    
    # Menambahkan kolom pencarian
    search_fields = ('komentar', 'user__username', 'produk__nama')

# Daftarkan model dan konfigurasi adminnya
admin.site.register(Ulasan, UlasanAdmin)