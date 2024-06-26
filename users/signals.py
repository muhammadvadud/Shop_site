from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.shortcuts import redirect, get_object_or_404
from .models import Cart, CartItem
from produtc.models import Product


@receiver(user_logged_in)
def merge_cart_on_login(sender, user, request, **kwargs):
    session_cart = request.session.get('cart', {})
    if session_cart:
        cart, created = Cart.objects.get_or_create(user=user)
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
