from django.views import View
from django.shortcuts import render, get_object_or_404
from produtc.models import Product, Category
from django.db.models import Count
from users.models import CartItem
from users.views import cart_view
import random


def get_top_selling_products():
    return Product.objects.all().order_by('-sales')[:10]  # Eng ko'p sotilgan 10 mahsulot


def get_latest_products():
    return Product.objects.all().order_by('-date')[:10]  # Eng yangi 10 mahsulot


def get_random_products():
    count = Product.objects.aggregate(count=Count('id'))['count']
    # Agar yozuvlar soni 10 dan kam bo'lsa, u holda mavjud yozuvlar sonini tanlang
    random_count = min(count, 20)
    random_indices = random.sample(range(count), random_count)
    return [Product.objects.all()[i] for i in random_indices]


# def load_more_products(request):
#     offset = int(request.GET.get('offset', 0))
#     limit = 20
#     products = Product.objects.all()[offset:offset + limit]
#     return render(request, 'products_list.html', {'products': products})


def get_all_product_categories():
    top_selling_products = get_top_selling_products()
    latest_products = get_latest_products()
    random_products = get_random_products()
    return {
        'top_selling': top_selling_products,
        'latest': latest_products,
        'random': random_products,
    }


def for_all_pages(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    cart_items = CartItem.objects.all()
    context = {
        "category": categories,
        "product": products,
        'items': cart_items,
    }
    return context


class IndexView(View):

    def get(self, request):
        product = get_all_product_categories()
        return render(request, 'index.html', product)


class CategoryView(View):
    def get(self, request, category_name):
        category = get_object_or_404(Category, name=category_name)
        product = Product.objects.filter(category=category)
        return render(request, "category.html", {'category': category, 'product': product})
