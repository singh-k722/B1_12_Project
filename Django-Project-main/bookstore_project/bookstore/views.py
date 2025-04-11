from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Book
from .forms import LoginForm

def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookstore/book_list.html', {'books': books})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('book_list')
    else:
        form = LoginForm()
    return render(request, 'bookstore/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def add_to_cart(request, book_id):
    cart = request.session.get('cart', [])
    if book_id not in cart:
        cart.append(book_id)
    request.session['cart'] = cart
    return redirect('book_list')

@login_required
def cart_view(request):
    cart = request.session.get('cart', [])
    books = Book.objects.filter(id__in=cart)
    return render(request, 'bookstore/cart.html', {'books': books})

