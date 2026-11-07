import requests
import base64
import uuid
import json
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order, OrderItem
from main.models import Produk
from django.http import JsonResponse

@login_required(login_url='/login/')
def halaman_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    
    total_harga = sum(item.total_harga_item() for item in items)
    total_qty = sum(item.quantity for item in items)

    context = {
        'items': items,
        'total_harga': total_harga,
        'total_qty': total_qty
    }
    return render(request, 'cart/cart.html', context)

@login_required(login_url='/login/')
def tambah_ke_cart(request, produk_id):
    produk = get_object_or_404(Produk, id=produk_id)
    
    # Hanya proses jika stok masih ada
    if produk.stok > 0:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, produk=produk)
        
        # Jika item sudah ada di keranjang, cek apakah kuantitas masih di bawah stok
        if not item_created:
            if cart_item.quantity < produk.stok:
                cart_item.quantity += 1
                cart_item.save()
            
    return redirect('halaman_cart')

@login_required(login_url='/login/')
def update_cart_item(request, item_id, action):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if action == 'tambah':
        # Batasi penambahan agar tidak melebihi stok produk
        if cart_item.quantity < cart_item.produk.stok:
            cart_item.quantity += 1
            cart_item.save()
    elif action == 'kurang':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            
    return redirect('halaman_cart')

@login_required(login_url='/login/')
def proses_checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()
    
    if not items.exists():
        return redirect('halaman_cart')
        
    total_harga = sum(item.total_harga_item() for item in items)
    order_id = f"TRX-{request.user.username}-{uuid.uuid4().hex[:6].upper()}"
    
    # Buat pesanan dengan alamat kosong terlebih dahulu
    order = Order.objects.create(
        user=request.user, order_id=order_id,
        total_harga=total_harga, status='Belum Dibayar'
    )
    
    for item in items:
        OrderItem.objects.create(order=order, produk=item.produk, harga_saat_beli=item.produk.harga, quantity=item.quantity)
        
    cart.items.all().delete()
    
    # Arahkan ke halaman pengisian alamat
    return redirect('isi_alamat', order_id=order.order_id)

@login_required(login_url='/login/')
def checkout_langsung(request, produk_id):
    produk = get_object_or_404(Produk, id=produk_id)
    if produk.stok <= 0:
        return redirect('detail_produk', produk_id=produk.id)
        
    order_id = f"TRX-DIR-{request.user.username}-{uuid.uuid4().hex[:6].upper()}"
    
    # Buat pesanan dengan alamat kosong terlebih dahulu
    order = Order.objects.create(
        user=request.user, order_id=order_id,
        total_harga=produk.harga, status='Belum Dibayar'
    )
    
    OrderItem.objects.create(order=order, produk=produk, harga_saat_beli=produk.harga, quantity=1)
    
    # Arahkan ke halaman pengisian alamat
    return redirect('isi_alamat', order_id=order.order_id)

@login_required(login_url='/login/')
def halaman_pembayaran(request, order_id):
    # Ambil pesanan berdasarkan ID dan pastikan itu milik user yang sedang login
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'cart/pembayaran.html', {'order': order})

@login_required(login_url='/login/')
def cek_status_pesanan(request, order_id):
    # Fungsi ini akan di-ping oleh JavaScript setiap 5 detik
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return JsonResponse({'status': order.status})

@login_required(login_url='/login/')
def pembayaran_berhasil(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'cart/pembayaran_berhasil.html', {'order': order})

@login_required(login_url='/login/')
def isi_alamat(request, order_id):
    # Tampilkan form pengisian alamat
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'cart/isi_alamat.html', {'order': order})

@login_required(login_url='/login/')
def simpan_alamat(request, order_id):
    # Proses penyimpanan alamat dari form
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    if request.method == 'POST':
        alamat = request.POST.get('alamat')
        order.alamat = alamat
        order.save() # Simpan alamat ke database
        
        # Setelah alamat tersimpan, arahkan ke halaman QR Code pembayaran
        return redirect('halaman_pembayaran', order_id=order.order_id)
        
    return redirect('isi_alamat', order_id=order.order_id)

@login_required(login_url='/login/')
def tracking_order(request):
    # Mengambil semua pesanan milik user ini, diurutkan dari yang terbaru (tanda minus)
    orders = Order.objects.filter(user=request.user).order_by('-tanggal_pesanan')
    return render(request, 'cart/tracking_order.html', {'orders': orders})