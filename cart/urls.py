from django.urls import path
from .views import CartView, AddToCartView, UpdateCartItemView, RemoveCartItemView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),                 # GET cart
    path('add/', AddToCartView.as_view(), name='add-to-cart'), # POST add item
    path('update/', UpdateCartItemView.as_view(), name='update-cart'),
    path('remove/', RemoveCartItemView.as_view(), name='remove-cart'),
]