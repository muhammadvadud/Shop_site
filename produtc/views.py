from django.shortcuts import render, redirect
from produtc.forms import NewProductForms, UpdateProductForms, ProductReviewForms
from produtc.models import ProductImage, Product, ProductReview
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.db.models import Avg
from django.http import JsonResponse


def superuser_check(user):
    return user.is_superuser


@login_required(login_url=reverse_lazy('login'))
@user_passes_test(superuser_check)
def new_product(request):
    if request.method == 'GET':
        form = NewProductForms
        return render(request, 'product_new.html', {'form': form})
    elif request.method == 'POST':
        form = NewProductForms(data=request.POST, files=request.FILES)
        if form.is_valid():
            product = form.save(request)
            for image in request.FILES.getlist('images'):
                ProductImage.objects.create(image=image, product=product)
            return redirect('main:index')
        return render(request, 'product_new.html', {'form': form})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_superuser:
        if request.method == 'POST':
            if 'delete' in request.POST:
                product.delete()
            return redirect('main:index')

    # Reting view
    reviews = ProductReview.objects.filter(product=product).order_by('-date')

    reviews_form = ProductReviewForms()

    context = {
        'product': product,
        'reviews': reviews,
        'reviews_form': reviews_form,
    }
    return render(request, 'product_detail.html', context)


# def ajax_add_review(request, pid):
#     product = Product.objects.get(pk=pid)
#     user = request.user
#
#     review = ProductReviewForms.objects.create(
#         user=user,
#         product=product,
#         review=request.POST['review'],
#         rating=request.POST['rating'],
#     )
#
#     context = {
#         'user': user.username,
#         'review': request.POST['review'],
#         'rating': request.POST['rating'],
#     }
#
#     average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
#
#     return JsonResponse({
#         'bool': True,
#         'context': context,
#         'average_reviews': average_reviews,
#
#     })
#
#     return render('index2.html', context)


@login_required(login_url=reverse_lazy('login'))
@user_passes_test(superuser_check)
def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if superuser_check:
        if request.method == "GET":
            form = UpdateProductForms(instance=product)
            return render(request, 'product_update.html', {'form': form})
        elif request.method == "POST":
            form = UpdateProductForms(instance=product, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                if request.FILES.getlist('images'):
                    ProductImage.objects.filter(product=product).delete()
                    for i in request.FILES.getlist('images'):
                        ProductImage.objects.create(product=product, image=i)
                return redirect('product:product_detail', product.id)
            return render(request, 'product_update.html', {'form': form})
    else:
        return redirect('main:index')
