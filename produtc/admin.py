from django.contrib import admin
from .models import Product, Category, ProductImage, ProductReview
from django.contrib.auth.admin import Group


class ProdutcImageInline(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'date', 'category', 'author']
    inlines = [ProdutcImageInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.unregister(Group)


@admin.register(ProductReview)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'rating', 'date']
    readonly_fields = ['date']
