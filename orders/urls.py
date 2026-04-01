from django.urls import path
from .views import PlaceOrderView, UserOrdersView, OrderDetailView

urlpatterns = [
    path('place/', PlaceOrderView.as_view()),
    path('', UserOrdersView.as_view()),
    path('<int:order_id>/', OrderDetailView.as_view()),
]

