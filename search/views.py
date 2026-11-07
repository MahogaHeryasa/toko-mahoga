from django.db.models import Q
from django.shortcuts import render

from main.models import Produk


def search_products(request):
    query = request.GET.get("q", "").strip()
    products = Produk.objects.none()

    if query:
        products = Produk.objects.filter(
            Q(nama__icontains=query)
            | Q(deskripsi__icontains=query)
            | Q(kategori__nama__icontains=query)
        ).select_related("kategori")

    return render(request, "search/search.html", {
        "query": query,
        "products": products,
    })
