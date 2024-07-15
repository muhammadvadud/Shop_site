from django.contrib import admin
from django.urls import path
from .views import IndexView, CategoryView, upload_products

app_name = 'main'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<str:category_name>/', CategoryView.as_view(), name='category'),
    path('upload-products/', upload_products, name='upload_products'),
]
