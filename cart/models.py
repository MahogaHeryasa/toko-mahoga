from django.db import models
from django.contrib.auth.models import User
from main.models import Produk # Mengimpor model Produk dari app utama

class Cart(models.Model):
    # OneToOne berarti 1 Akun hanya memiliki 1 Keranjang utama
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Keranjang milik {self.user.username}"

class CartItem(models.Model):
    # Menghubungkan isi produk ke keranjangnya
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    # Fungsi pembantu untuk menghitung sub-total (harga x jumlah)
    def total_harga_item(self):
        return self.produk.harga * self.quantity

class Order(models.Model):
    STATUS_CHOICES = (
        ('Belum Dibayar', 'Belum Dibayar'),
        ('Lunas', 'Lunas'),
        ('Dikemas', 'Dikemas'),
        ('Dikirim', 'Dikirim'),
        ('Diterima', 'Diterima'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, unique=True)
    total_harga = models.DecimalField(max_digits=12, decimal_places=2)
    alamat = models.TextField(default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Belum Dibayar')
    tanggal_pesanan = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_id} - {self.status}"

    # --- TAMBAHKAN FUNGSI SAVE INI ---
    def save(self, *args, **kwargs):
        # Cek apakah pesanan ini sudah pernah tersimpan di database sebelumnya
        if self.pk:
            # Ambil data pesanan yang lama (sebelum tombol save ditekan)
            pesanan_lama = Order.objects.get(pk=self.pk)
            
            # Jika status sebelumnya BUKAN 'Lunas', dan sekarang diubah MENJADI 'Lunas'
            if pesanan_lama.status != 'Lunas' and self.status == 'Lunas':
                
                # Looping semua barang yang ada di dalam pesanan ini
                for item in self.items.all():
                    # Pastikan produknya belum dihapus dari etalase
                    if item.produk:
                        # Kurangi stok produk sebanyak quantity yang dibeli
                        item.produk.stok -= item.quantity
                        item.produk.save()
                        
        # Lanjutkan proses penyimpanan bawaan Django
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    harga_saat_beli = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.IntegerField(default=1)
    
    # TAMBAHKAN BARIS INI
    sudah_diulas = models.BooleanField(default=False) 

    def total_harga_item(self):
        return self.harga_saat_beli * self.quantity