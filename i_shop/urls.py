from django.urls import path

from . import views

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='home'),
    path('cart/', views.cart, name='cart'),
    path('<slug:slug>/', views.ProductListView.as_view(), name='product_list'),
    path('<slug:slug>/<slug:product_slug>', views.ProductDetailView.as_view(), name='product_detail'),

]
