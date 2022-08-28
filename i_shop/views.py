from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Category, Product


def cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = []
    request.session['cart'].append({'id': 1, 'quantity': 10})
    request.session['cart'].append({'id': 2, 'quantity': 10})
    # print(request.session['cart'])
    products = []
    for i in request.session['cart']:
        product = Product.objects.get(pk=i['id'])
        products.append(product)
    context = {'products': products, 'cart': cart}
    return render(request, template_name='i_shop/cart.html', context=context)


def add_to_cart(request):
    pass


class CategoryListView(ListView):
    model = Category


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs.get("slug"))


class ProductDetailView(DetailView):
    model = Product
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'
    template_name = 'i_shop/product_detail.html'

