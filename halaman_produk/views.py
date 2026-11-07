from django.shortcuts import render, get_object_or_404
from main.models import Produk # Mengambil model dari app pertama

def detail_produk(request, id):
    # Mengambil 1 produk berdasarkan ID, jika tidak ada tampilkan 404
    item = get_object_or_404(Produk, id=id) 
    return render(request, 'halaman_produk/detail.html', {'produk': item})