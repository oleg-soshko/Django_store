from typing import NamedTuple

from .models import Product


class CartItems(NamedTuple):
    products_in_cart: list
    to_pay: int
    quantity_in_cart: int


def add(request, id, product_quantity=1):
    if request.method == 'POST':
        if not request.session.get('cart'):
            request.session['cart'] = list()
        else:
            request.session['cart'] = list(request.session['cart'])

        add_data = {
            'product_id': id,
            'quantity': product_quantity
        }

        product_exists = next((product for product in request.session['cart'] if product['product_id'] == id), False)

        if not product_exists:
            request.session['cart'].append(add_data)
            request.session.modified = True
        else:
            for product in request.session['cart']:
                if product['product_id'] == id:
                    product['quantity'] += product_quantity
                    request.session.modified = True


def remove(request, id):
    if request.method == 'GET':
        for product in request.session['cart']:
            if product['product_id'] == id:
                product.clear()
        while {} in request.session['cart']:
            request.session['cart'].remove({})
    request.session.modified = True


def get_cart_content(request):
    products_in_cart = list()
    to_pay = 0
    quantity_in_cart = 0
    if not request.session.get('cart'):
        request.session['cart'] = list()
    else:
        for item in request.session['cart']:
            product_in_cart = Product.objects.get(pk=int(item['product_id']))
            total = item['quantity'] * product_in_cart.price
            to_pay += total
            quantity_in_cart += item['quantity']
            products_in_cart.append(
                {'product': product_in_cart,
                 'quantity': item['quantity'],
                 'total': total
                 }
            )
    #return products_in_cart, to_pay, quantity_in_cart
    return CartItems(products_in_cart=products_in_cart, to_pay=to_pay, quantity_in_cart=quantity_in_cart)


def delete_cart(request):
    if request.session.get('cart'):
        del request.session['cart']
        request.session.modified = True
