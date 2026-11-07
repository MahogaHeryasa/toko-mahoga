from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

# --- TAMBAHKAN MODEL INI ---
class Kategori(models.Model):
    nama = models.CharField(max_length=100)
    slug = models.SlugField(unique=True) # Slug digunakan untuk nama di URL (misal: /?kategori=gitar-akustik)

    def __str__(self):
        return self.nama

# --- UPDATE MODEL PRODUK ---
class Produk(models.Model):
    # Tambahkan baris kategori ini:
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True, blank=True)
    
    nama = models.CharField(max_length=200)
    deskripsi = models.TextField()
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    stok = models.IntegerField(default=0)
    gambar = models.ImageField(upload_to='produk/', null=True, blank=True)

    def __str__(self):
        return self.nama

class GambarProduk(models.Model):
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE, related_name='galeri')
    gambar_tambahan = models.ImageField(upload_to='produk/galeri/')

    def __str__(self):
        return f"Galeri: {self.produk.nama}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    foto = models.ImageField(upload_to="profiles/", null=True, blank=True)

    def __str__(self):
        return f"Profil: {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# HAPUS parameter gambar di model Ulasan Anda menjadi seperti ini:
class Ulasan(models.Model):
    produk = models.ForeignKey(Produk, related_name='ulasan', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    komentar = models.TextField()
    # (Kolom 'gambar = models.ImageField...' HAPUS SAJA DARI SINI)
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ulasan {self.user.username} - {self.produk.nama}"

# TAMBAHKAN MODEL BARU INI DI BAWAHNYA:
class GambarUlasan(models.Model):
    ulasan = models.ForeignKey(Ulasan, related_name='gambar_ulasan', on_delete=models.CASCADE)
    gambar = models.ImageField(upload_to='ulasan/')