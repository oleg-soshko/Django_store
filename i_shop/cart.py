from .models import Product


def add(request, id):
    if request.method == 'POST':
        if not request.session.get('cart'):
            request.session['cart'] = list()
        else:
            request.session['cart'] = list(request.session['cart'])

        add_data = {
            'product_id': id,
            'quantity': 1
        }

        product_exists = next((product for product in request.session['cart'] if product['product_id'] == id), False)

        if not product_exists:
            request.session['cart'].append(add_data)
            request.session.modified = True
        else:
            for product in request.session['cart']:
                if product['product_id'] == id:
                    product['quantity'] += 1
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
    return products_in_cart, to_pay, quantity_in_cart
