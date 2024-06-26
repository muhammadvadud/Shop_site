from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_nubmer = models.CharField(max_length=100)
    tg_username = models.CharField(max_length=150)
    avatar = models.ImageField(upload_to="avatars/", default="avatars/avatar_default.png")

    def __str__(self):
        return str(self.username)


class Wishes(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey('produtc.Product', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Wishes of " + str(self.author.username)


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('produtc.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price
