from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import CheckoutForm, UserRegisterForm, UserLoginForm
from .models import Category, Product, Order, OrderDetails
from .cart import add, remove, get_cart_content, delete_cart


class CategoryListView(ListView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_content = get_cart_content(self.request)
        context['products'] = cart_content.products_in_cart
        context['to_pay'] = cart_content.to_pay
        context['quantity_in_cart'] = cart_content.quantity_in_cart
        return context


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_content = get_cart_content(self.request)
        context['products'] = cart_content.products_in_cart
        context['to_pay'] = cart_content.to_pay
        context['quantity_in_cart'] = cart_content.quantity_in_cart
        return context


class ProductDetailView(DetailView):
    model = Product
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'
    template_name = 'i_shop/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_content = get_cart_content(self.request)
        context['products'] = cart_content.products_in_cart
        context['to_pay'] = cart_content.to_pay
        context['quantity_in_cart'] = cart_content.quantity_in_cart
        return context


class Cart(View):
    def get(self, request):
        if not request.session.get('cart'):
            request.session['cart'] = list()
        cart_content = get_cart_content(request)
        return render(request, 'i_shop/cart.html', {'products': cart_content.products_in_cart,
                                                    'to_pay': cart_content.to_pay,
                                                    'quantity_in_cart': cart_content.quantity_in_cart})


def add_to_cart(request, product_id):
    product_quantity = int(request.POST.get('product_quantity'))
    add(request, product_id, product_quantity)
    return redirect('cart')


def quick_add_to_cart(request, product_id):
    add(request, product_id)
    messages.success(request, 'Товар добавлен в корзину')
    return redirect(request.POST.get('url_from'))


def remove_from_cart(request, product_id):
    remove(request, product_id)
    return redirect('cart')


def checkout(request):
    if not request.session.get('cart'):
        request.session['cart'] = list()
    cart_content = get_cart_content(request)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                city=form.cleaned_data['city'],
                address=form.cleaned_data['address'],
                payment_type=form.cleaned_data['payment_type'],
                delivery_type=form.cleaned_data['delivery_type'],
                total_price=cart_content.to_pay,
                total_to_pay=cart_content.to_pay + form.cleaned_data['delivery_type'].cost,
                user=request.user
            )
            for item in cart_content[0]:
                OrderDetails.objects.create(
                    product=item['product'],
                    quantity=item['quantity'],
                    order=order
                )
            return redirect('success', order_pk=order.pk)
            #Order.objects.create(**form.cleaned_data)
            # city = form.cleaned_data['city']
            # Order.objects.create(city=city)
    else:
        form = CheckoutForm()
    return render(request, 'i_shop/checkout.html', {'form': form,
                                                    'products': cart_content.products_in_cart,
                                                    'to_pay': cart_content.to_pay,
                                                    'quantity_in_cart': cart_content.quantity_in_cart})


def success(request, order_pk):
    if not request.session.get('cart'):
        request.session['cart'] = list()
    cart_content = get_cart_content(request)
    order_date = datetime.now().strftime("%d.%m.%y")
    order = Order.objects.get(pk=order_pk)
    delete_cart(request)
    return render(request, 'i_shop/success.html', {'products': cart_content.products_in_cart,
                                                   'to_pay': cart_content.to_pay,
                                                   'quantity_in_cart': cart_content.quantity_in_cart,
                                                   'order_date': order_date,
                                                   'order': order})


def register(request):
    if not request.session.get('cart'):
        request.session['cart'] = list()
    cart_content = get_cart_content(request)
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'i_shop/register.html', {'form': form,
                                                    'products': cart_content.products_in_cart,
                                                    'to_pay': cart_content.to_pay,
                                                    'quantity_in_cart': cart_content.quantity_in_cart})


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
    return render(request, 'i_shop/login.html', {'form': form,
                                                 'products': cart_content.products_in_cart,
                                                 'to_pay': cart_content.to_pay,
                                                 'quantity_in_cart': cart_content.quantity_in_cart})


def user_logout(request):
    logout(request)
    return redirect('login')


class UserMenuInfo(View):
    def get(self, request):
        if not request.session.get('cart'):
            request.session['cart'] = list()
        cart_content = get_cart_content(request)

        return render(request, 'i_shop/user_menu_info.html', {'user': request.user,
                                                              'products': cart_content.products_in_cart,
                                                              'to_pay': cart_content.to_pay,
                                                              'quantity_in_cart': cart_content.quantity_in_cart})


class UserMenuOrders(View):
    def get(self, request):
        if not request.session.get('cart'):
            request.session['cart'] = list()
        cart_content = get_cart_content(request)
        orders = Order.objects.all()

        return render(request, 'i_shop/user_menu_orders.html', {'user': request.user,
                                                                'orders': orders,
                                                                'products': cart_content.products_in_cart,
                                                                'to_pay': cart_content.to_pay,
                                                                'quantity_in_cart': cart_content.quantity_in_cart})
