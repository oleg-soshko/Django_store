from django.urls import path

from . import views

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/<order_pk>', views.success, name='success'),
    path('<slug:slug>/', views.ProductListView.as_view(), name='product_list'),
    path('<slug:slug>/<slug:product_slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('quick_add_to_cart/<product_id>/', views.quick_add_to_cart, name='quick_add'),
    path('add/<product_id>/', views.add_to_cart, name='add'),
    path('remove/<product_id>/', views.remove_from_cart, name='remove'),
]
