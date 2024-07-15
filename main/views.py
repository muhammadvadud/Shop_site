from django.views import View
from django.shortcuts import render, get_object_or_404
from produtc.models import Product, Category, ProductImage
from django.db.models import Count
from users.models import CartItem, CustomUser
from users.views import cart_view
from django.http import HttpResponse, HttpResponseRedirect
import csv
import random


def get_top_selling_products():
    return Product.objects.all().order_by('-sales')[:10]  # Eng ko'p sotilgan 10 mahsulot


def get_latest_products():
    return Product.objects.all().order_by('-date')[:30]  # Eng yangi 10 mahsulot


def get_random_products():
    count = Product.objects.aggregate(count=Count('id'))['count']
    # Agar yozuvlar soni 10 dan kam bo'lsa, u holda mavjud yozuvlar sonini tanlang
    random_count = min(count, 40)
    random_indices = random.sample(range(count), random_count)
    return [Product.objects.all()[i] for i in random_indices]


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


def upload_products(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        errors = []
        for row in reader:
            try:
                author = CustomUser.objects.get(username=row['author'])
            except CustomUser.DoesNotExist:
                errors.append(f"User {row['author']} does not exist.")
                continue

            # Tekshirish va kategoriya yaratish yoki topish
            category_name = row['category']
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                category.save()

            product = Product(
                author=author,
                category=category,
                title=row['title'],
                description=row['description'],
                price=row['price'],
                address=row['address'],
                phone_number=row['phone_number'],
                tg_username=row['tg_username'],
                discount=row.get('discount', None),
                sales=row.get('sales', 0)
            )
            product.save()

            image_urls = row.get('image_urls', '').split(';')
            for image_url in image_urls:
                ProductImage.objects.create(product=product, image=image_url)

        if errors:
            return HttpResponse(f"Errors encountered: {', '.join(errors)}")
        return HttpResponse("Products have been uploaded successfully")

    return render(request, 'upload_products.html')
