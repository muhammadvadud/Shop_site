from django.urls import path
from .views import SignupView, ProfileView, AddRemoveWishesView, WishesView, CheckWishStatusView, cart_view, \
    add_to_cart, merge_cart, remove_from_cart

app_name = 'users'
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('AddRemoveWishes/<int:product_id>/', AddRemoveWishesView.as_view(), name='addremovewishes'),
    path('CheckWishStatus/<int:product_id>/', CheckWishStatusView.as_view(), name='checkwishstatus'),
    path('wishes/', WishesView.as_view(), name='wishes'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart_view, name='cart'),
    path('merge_cart/', merge_cart, name='merge_cart'),
]
