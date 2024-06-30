from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Product, CartItem
from .forms import AddToCartForm, CustomUserCreationForm

def home(request):
    products = Product.objects.all()
    return render(request, 'internet-shop-pc.html', {'products': products})

def information_view(request):
    latest_products = Product.objects.order_by('-id')[:6]  # Получаем последние 6 добавленных товаров
    return render(request, 'information.html', {'latest_products': latest_products})

def where_to_find_us_view(request):
    return render(request, 'where_to_find_us.html')

from django.shortcuts import render
from .models import Product

def catalog_view(request):
    products = Product.objects.all()
    
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    return render(request, 'catalog.html', {'products': products})


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = AddToCartForm()
    latest_products = Product.objects.order_by('-id')[:5]  # Получаем последние 5 добавленных товаров
    return render(request, 'product_detail.html', {'product': product, 'form': form, 'latest_products': latest_products})   

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Неверный логин или пароль.')
        else:
            messages.error(request, 'Неверный логин или пароль.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def success_view(request):
    return render(request, 'success.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
            if not created:
                cart_item.quantity += form.cleaned_data['quantity']
            else:
                cart_item.quantity = form.cleaned_data['quantity']
            cart_item.save()
            messages.success(request, 'Товар добавлен в корзину.')
            return redirect('cart')
        else:
            messages.error(request, 'Ошибка при добавлении товара в корзину.')
    else:
        form = AddToCartForm(initial={'product': product})
    return render(request, 'add_to_cart.html', {'form': form, 'product': product})

@login_required
def remove_from_cart_view(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    if request.method == 'POST':
        cart_item.delete()
        messages.success(request, 'Товар удален из корзины.')
    return redirect('cart')
