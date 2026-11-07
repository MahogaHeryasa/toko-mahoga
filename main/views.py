from django.shortcuts import render
from .models import Produk, Kategori, Ulasan, GambarUlasan
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import AccountForm, AccountPasswordForm, ProfileForm
from .models import Profile
from cart.models import OrderItem
from django.shortcuts import render, redirect, get_object_or_404

def daftar_produk(request):
    # Menangkap parameter 'kategori' dari URL
    kategori_slug = request.GET.get('kategori')
    semua_kategori = Kategori.objects.all()
    
    # Jika ada parameter kategori, filter produknya. Jika tidak, tampilkan semua.
    if kategori_slug:
        semua_produk = Produk.objects.filter(kategori__slug=kategori_slug)
    else:
        semua_produk = Produk.objects.all()

    context = {
        'produk': semua_produk,
        'kategori_list': semua_kategori,
        'kategori_aktif': kategori_slug, # Untuk menandai menu kategori yang sedang aktif
    }
    return render(request, 'main/daftar_produk.html', context)

# Fungsi Registrasi
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Langsung otomatis login setelah sukses daftar
            return redirect('halaman_cart')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})

# Fungsi Logout
def logout_user(request):
    logout(request)
    return redirect('/') # Kembali ke halaman utama setelah logout


@login_required(login_url='login')
def account_page(request):
    Profile.objects.get_or_create(user=request.user)
    return render(request, 'main/account.html')


@login_required(login_url='login')
def edit_account(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST' and request.POST.get('form_type') == 'password':
        account_form = AccountForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
        password_form = AccountPasswordForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect('account')
    elif request.method == 'POST':
        form = AccountForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return redirect('account')
        account_form = form
        password_form = AccountPasswordForm(request.user)
    else:
        account_form = AccountForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
        password_form = AccountPasswordForm(request.user)

    return render(request, 'main/edit_account.html', {
        'form': account_form,
        'profile_form': profile_form,
        'password_form': password_form,
    })


@login_required(login_url='/login/')
def tambah_ulasan(request, produk_id):
    produk = get_object_or_404(Produk, id=produk_id)
    
    # 1. Cari riwayat pembelian item ini yang BELUM diulas
    order_item = OrderItem.objects.filter(
        order__user=request.user, 
        order__status='Diterima', 
        produk=produk,
        sudah_diulas=False # Pastikan belum diulas
    ).first()
    
    # Jika tidak ada pesanan terkait atau sudah diulas, kembalikan ke detail
    if not order_item:
        return redirect('detail_produk', id=produk.id)
        
    if request.method == 'POST':
        rating = request.POST.get('rating')
        komentar = request.POST.get('komentar')
        
        ulasan_baru = Ulasan.objects.create(
            produk=produk, 
            user=request.user, 
            rating=rating, 
            komentar=komentar
        )
        
        gambar_multiple = request.FILES.getlist('gambar')
        for file_gambar in gambar_multiple:
            GambarUlasan.objects.create(ulasan=ulasan_baru, gambar=file_gambar)
            
        # 2. TANDAI ITEM INI SUDAH DIULAS
        order_item.sudah_diulas = True
        order_item.save()
            
        return redirect('detail_produk', id=produk.id)
        
    return render(request, 'main/tambah_ulasan.html', {'produk': produk})