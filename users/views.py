from django.shortcuts import render, redirect
from users.forms import SignupForm, UpdateProfileForm
from django.views import View
from django.urls import reverse
from django.shortcuts import get_object_or_404
from users.models import CustomUser, Wishes, CartItem, Cart
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from produtc.models import Product
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


class SignupView(UserPassesTestMixin, View):
    def get(self, request):
        return render(request, 'account/signup.html', {'form': SignupForm()})

    def post(self, request):
        form = SignupForm(data=request.POST)
        if form.is_valid():
            form.save()
        username = form.data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect(reverse('main:index'))
        return render(request, 'account/signup.html', {'form': form})

    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            return False
        return True


class ProfileView(View):

    def get(self, request):
        user = get_object_or_404(CustomUser, id=request.user.id)
        registration_date = request.user.date_joined
        form = UpdateProfileForm(instance=request.user)
        return render(request, 'profile.html', {'customuser': user, 'user_date': registration_date, 'form': form})

    def post(self, request):
        form = UpdateProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
        return render(request, 'profile.html', {'form': form})


class AddRemoveWishesView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            wishes = Wishes.objects.filter(author=request.user, product=product)
            if wishes.exists():
                wishes.delete()
                messages.info(request, 'O`chirildi.')
                return JsonResponse({'status': 'removed'})
            else:
                Wishes.objects.create(author=request.user, product=product)
                messages.info(request, 'Qo`shildi.')
                return JsonResponse({'status': 'added'})
        else:
            # Ro'yxatdan o'tmagan foydalanuvchilar uchun
            wishlist = request.session.get('wishlist', [])
            if product_id in wishlist:
                wishlist.remove(product_id)
                messages.info(request, 'O`chirildi.')
                request.session['wishlist'] = wishlist
                return JsonResponse({'status': 'removed'})
            else:
                wishlist.append(product_id)
                messages.info(request, 'Qo`shildi.')
                request.session['wishlist'] = wishlist
                return JsonResponse({'status': 'added'})

        return redirect(request.META.get('HTTP_REFERER'))

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            wishes_product = Wishes.objects.filter(author=request.user, product=product)
            if request.method == 'POST':
                wishes_product.delete()
                messages.info(request, 'O`chirildi')
                return redirect('users:wishes')
        else:
            # Ro'yxatdan o'tmagan foydalanuvchilar uchun
            wishlist = request.session.get('wishlist', [])
            if product_id in wishlist:
                wishlist.remove(product_id)
                messages.info(request, 'O`chirildi.')
                request.session['wishlist'] = wishlist
        return redirect('users:wishes')


class CheckWishStatusView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            wishes = Wishes.objects.filter(author=request.user, product=product)
            if wishes.exists():
                return JsonResponse({'status': 'liked'})
            else:
                return JsonResponse({'status': 'not_liked'})
        else:
            # Ro'yxatdan o'tmagan foydalanuvchilar uchun
            wishlist = request.session.get('wishlist', [])
            if product_id in wishlist:
                return JsonResponse({'status': 'liked'})
            else:
                return JsonResponse({'status': 'not_liked'})


class WishesView(View):
    def get(self, request):
        if request.user.is_authenticated:
            wished = Wishes.objects.filter(author=request.user).order_by('-id')
        else:
            # Ro'yxatdan o'tmagan foydalanuvchilar uchun
            wishlist = request.session.get('wishlist', [])
            wished = Product.objects.filter(id__in=wishlist)

        return render(request, 'wishes.html', {'wished': wished})


# views.py


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
    else:
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        else:
            cart[str(product_id)] = {'product_id': product.id, 'quantity': 1}
        request.session['cart'] = cart
    return JsonResponse({'status': 'added'})


def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        cart_item.delete()
    else:
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            del cart[str(product_id)]
            request.session['cart'] = cart
    return JsonResponse({'status': 'removed'})


def cart_view(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
    else:
        cart = request.session.get('cart', {})
        product_ids = [item['product_id'] for item in cart.values()]
        products = Product.objects.filter(id__in=product_ids)
        cart_items = [{'product': product, 'quantity': cart[str(product.id)]['quantity']} for product in products]

    if not cart_items:
        return render(request, 'cart.html', {'cart_items': cart_items, 'total': 0, 'is_empty': True})

    total = sum(
        item.total_price() if request.user.is_authenticated else item['quantity'] * item['product'].price for item in
        cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total, 'is_empty': False})


@login_required
def merge_cart(request):
    session_cart = request.session.get('cart', {})
    if session_cart:
        cart, created = Cart.objects.get_or_create(user=request.user)
        for item in session_cart.values():
            product = get_object_or_404(Product, id=item['product_id'])
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if created:
                cart_item.quantity = item['quantity']
            else:
                cart_item.quantity += item['quantity']
            cart_item.save()
        request.session['cart'] = {}
    return redirect('cart')
