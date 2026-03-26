from django.urls import path
from .views import ProductListCreateView,CategoryListCreateView, ProductVariantListCreateView

urlpatterns = [
    path('products/', ProductListCreateView.as_view()),
    path('categories/', CategoryListCreateView.as_view()), 
    path('variants/', ProductVariantListCreateView.as_view()), 
] 