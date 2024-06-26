from django.urls import path
from produtc.views import new_product, product_detail, product_update

app_name = 'product'
urlpatterns = [
    path('new_product/', new_product, name='new'),
    path('<int:product_id>/detail/', product_detail, name='product_detail'),
    path('<int:product_id>/update/', product_update, name='product_update'),
]

