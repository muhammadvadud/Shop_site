# from django.contrib.auth.models import User
from django.db import models
from users.models import CustomUser

Rating = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★'),

)


class Category(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='category_image/')

    def __str__(self):
        return self.name


class Product(models.Model):
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=1000000000, decimal_places=2)
    address = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=100)
    tg_username = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    discount = models.IntegerField(null=True, blank=True)
    sales = models.IntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ["-id"]


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=Rating, default=None)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Review'

    def __str__(self):
        return str(self.id)

    def get_rating(self):
        return self.rating
