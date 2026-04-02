from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Product
from django.db.models import Q
from decimal import Decimal, InvalidOperation
from orders.forms import OrderForm
from orders.models import OrderItem

def home(request):
    categories = Category.objects.all()
    return render(request, 'catalog/home.html', {'categories': categories})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'catalog/category_list.html', {'categories': categories})

def product_list_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    qs = Product.objects.filter(category=category, is_active=True).order_by('name')

    qs = qs.select_related('category').prefetch_related('images')

    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()

    try:
        if min_price:
            qs = qs.filter(price__gte=Decimal(min_price))
        if max_price:
            qs = qs.filter(price__lte=Decimal(max_price))
    except (InvalidOperation, ValueError):
        pass

    if request.GET.get("in_stock") == "1":
        qs = qs.filter(stock__gt=0)

    sort = request.GET.get("sort", "")
    
    if sort == "price_asc":
        qs = qs.order_by("price")
    elif sort == "price_desc":
        qs = qs.order_by("-price")
    elif sort == "new":
        qs = qs.order_by("-id")  # новинки сверху
    else:
        qs = qs.order_by("name")


    paginator = Paginator(qs, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    params = request.GET.copy()
    if 'page' in params:
        params.pop('page')
    qs_params = params.urlencode()

    return render(request, 'catalog/product_list.html', {
        'category': category,
        'page_obj': page_obj,
        'qs_params': qs_params,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'catalog/product_detail.html', {'product': product})

def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    cart = request.session.get('cart', {})
    product_id_str = str(product.id)
    if product_id_str in cart:
        if cart[product_id_str] < product.stock:
            cart[product_id_str] += 1
    else:
        if product.stock > 0:
            cart[product_id_str] = 1
 
    request.session['cart'] = cart
    request.session.modified = True

    return redirect('catalog:product_detail', slug=slug)

def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    items = []
    total = 0

    for product in products:
        quantity = cart.get(str(product.id), 0)
        price = product.price * quantity

        items.append({
            'product': product,
            'quantity': quantity,
            'price': price,
        })

        total += price

    return render(request, 'catalog/cart.html', {
        'items': items,
        'total': total,
    })


def checkout(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    items = []
    total = 0
    stock_errors = []

    for product in products:
        quantity = cart.get(str(product.id), 0)
        if quantity <= 0:
            continue
        if quantity > product.stock:
            stock_errors.append(f"Товар \"{product.name}\" доступен в количестве {product.stock}.")
        items.append({
            'product': product,
            'quantity': quantity,
            'price': product.price * quantity,
        })
        total += product.price * quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if not items:
            messages.error(request, "Корзина пуста. Добавьте товар перед оформлением заказа.")
        elif stock_errors:
            for error in stock_errors:
                messages.error(request, error)
        elif form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for item in items:
                product = item['product']
                quantity = item['quantity']
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price,
                )
                product.stock = product.stock - quantity
                if product.stock < 0:
                    product.stock = 0
                product.save(update_fields=['stock'])
            request.session['cart'] = {}
            request.session.modified = True
            return render(request, 'catalog/order_success.html', {'order': order})
    else:
        form = OrderForm()

    return render(request, 'catalog/checkout.html', {
        'form': form,
        'items': items,
        'total': total,
        'stock_errors': stock_errors,
    })


def remove_from_cart(request, slug):
    cart = request.session.get('cart', {})
    product_id_str = str(get_object_or_404(Product, slug=slug).id)

    if product_id_str in cart:
        del cart[product_id_str]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('catalog:cart')