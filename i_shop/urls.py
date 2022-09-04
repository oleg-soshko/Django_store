from django.urls import path

from . import views

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='home'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('<slug:slug>/', views.ProductListView.as_view(), name='product_list'),
    path('<slug:slug>/<slug:product_slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('quick_add_to_cart/<id>/', views.quick_add_to_cart, name='quick_add'),
    path('add/<id>/', views.add_to_cart, name='add'),
    path('remove/<id>/', views.remove_from_cart, name='remove'),

]
