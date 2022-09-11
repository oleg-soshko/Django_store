from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import CheckoutForm, UserRegisterForm, UserLoginForm
from .models import Category, Product
from .cart import add, remove, get_cart_content


class CategoryListView(ListView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_content = get_cart_content(self.request)
        context['products'] = cart_content[0]
        context['to_pay'] = cart_content[1]
        context['quantity_in_cart'] = cart_content[2]
        return context


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_content = get_cart_content(self.request)
        context['products'] = cart_content[0]
        context['to_pay'] = cart_content[1]
        context['quantity_in_cart'] = cart_content[2]
        return context


class ProductDetailView(DetailView):
    model = Product
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'
    template_name = 'i_shop/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_content = get_cart_content(self.request)
        context['products'] = cart_content[0]
        context['to_pay'] = cart_content[1]
        context['quantity_in_cart'] = cart_content[2]
        return context


class Cart(View):
    def get(self, request):
        if not request.session.get('cart'):
            request.session['cart'] = list()
        cart_content = get_cart_content(request)
        return render(request, 'i_shop/cart.html',
                      {'products': cart_content[0], 'to_pay': cart_content[1], 'quantity_in_cart': cart_content[2]})


def add_to_cart(request, product_id):
    add(request, product_id)
    return redirect('cart')


def quick_add_to_cart(request, product_id):
    add(request, product_id)
    return redirect(request.POST.get('url_from'))


def remove_from_cart(request, product_id):
    remove(request, product_id)
    return redirect('cart')


def checkout(request):
    if not request.session.get('cart'):
        request.session['cart'] = list()
    cart_content = get_cart_content(request)
    form = CheckoutForm()
    return render(request, 'i_shop/checkout.html', {'form': form, 'products': cart_content[0],
                                                    'to_pay': cart_content[1], 'quantity_in_cart': cart_content[2]})


def register(request):
    if not request.session.get('cart'):
        request.session['cart'] = list()
    cart_content = get_cart_content(request)
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You are register')
            return redirect('home')
        else:
            messages.error(request, 'Error register')
    else:
        form = UserRegisterForm()
    return render(request, 'i_shop/register.html', {'form': form, 'products': cart_content[0],
                                                    'to_pay': cart_content[1], 'quantity_in_cart': cart_content[2]})


def user_login(request):
    if not request.session.get('cart'):
        request.session['cart'] = list()
    cart_content = get_cart_content(request)
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'i_shop/login.html', {'form': form, 'products': cart_content[0],
                                                 'to_pay': cart_content[1], 'quantity_in_cart': cart_content[2]})


def user_logout(request):
    logout(request)
    return redirect('login')
