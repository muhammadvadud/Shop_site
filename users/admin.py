from django.contrib import admin
from .models import Wishes, CustomUser
from .models import Cart, CartItem

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishes)
admin.site.register(CustomUser)
