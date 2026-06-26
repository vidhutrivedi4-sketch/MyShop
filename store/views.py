from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# HOME
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


# PRODUCT DETAIL
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


# ADD TO CART
def add_to_cart(request, id):
    cart = request.session.get('cart', {})

    product_id = str(id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart
    return redirect('cart')

# CART
def cart(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for pid, qty in cart.items():
        try:
            product = Product.objects.get(id=pid)
            product.qty = qty
            product.total = product.price * qty
            total += product.total
            products.append(product)
        except Product.DoesNotExist:
            continue

    return render(request, 'cart.html', {
        'products': products,
        'total': total
    })
# REMOVE FROM CART (1 ITEM REMOVE)
def remove_from_cart(request, id):
    cart = request.session.get('cart', {})

    product_id = str(id)

    if product_id in cart:
        if cart[product_id] > 1:
            cart[product_id] -= 1   # 1 quantity kam
        else:
            del cart[product_id]    # 0 ho gaya to delete

    request.session['cart'] = cart
    return redirect('cart')

# CHECKOUT
# CHECKOUT PAGE (REPLACE OLD ONE COMPLETELY)
def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    total = 0

    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")

        order = Order.objects.create(
            user=request.user
        )

        for pid, qty in cart.items():
            product = Product.objects.get(id=pid)

            total += product.price * qty

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty
            )

        # clear cart
        request.session['cart'] = {}

        return redirect('success')

    # show checkout page
    products = []
    total = 0

    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        product.qty = qty
        product.total = product.price * qty
        total += product.total
        products.append(product)

    return render(request, 'checkout.html', {
        'products': products,
        'total': total
    })
    # PLACE ORDER
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")

        order = Order.objects.create(
            user=request.user
        )

        for pid, qty in cart.items():
            product = Product.objects.get(id=pid)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty
            )

        request.session['cart'] = {}

        return redirect('success')

# SUCCESS PAGE
def success(request):
    last_order = Order.objects.filter(user=request.user).last()

    order_items = []
    total = 0

    if last_order:
        order_items = OrderItem.objects.filter(order=last_order)

        for item in order_items:
            total += item.product.price * item.quantity

    return render(request, 'success.html', {
        'order': last_order,
        'items': order_items,
        'total': total
    })

# SEARCH
from django.db.models import Q

def search(request):
    query = request.GET.get('q')

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(category__name__icontains=query)
    )

    return render(request, 'home.html', {'products': products})

# REGISTER
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        User.objects.create_user(username=username, password=password)
        return redirect("login")

    return render(request, "registration/register.html")
# LOGIN
def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            error = "Wrong username or password"

    return render(request, "registration/login.html", {"error": error})
def remove_all_from_cart(request, id):
    cart = request.session.get('cart', {})

    product_id = str(id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    return redirect('cart')

# LOGOUT
def logout_view(request):
    logout(request)
    return redirect("home")

    # MY ORDERS
def my_orders(request):
    if not request.user.is_authenticated:
        return redirect('login')

    orders = Order.objects.filter(user=request.user).order_by('-id')

    return render(request, 'my_orders.html', {
        'orders': orders
    })