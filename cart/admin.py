from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('produk', 'harga_saat_beli', 'quantity') # Bersifat read-only agar riwayat tidak diubah

class OrderAdmin(admin.ModelAdmin):
    # Tambahkan 'alamat' di dalam list ini:
    list_display = ('order_id', 'user', 'total_harga', 'status', 'alamat', 'tanggal_pesanan')
    list_filter = ('status', 'tanggal_pesanan')
    search_fields = ('order_id', 'user__username')
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)