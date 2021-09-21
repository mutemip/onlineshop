from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Product
from .forms import SignupForm
from django.http import HttpResponseRedirect
from cart.forms import CartAddProductForm
from django.contrib import messages
from django.db.models import Q

from .recommender import Recommender


# Create your views here.
def customerlogin(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'username or password is incorrect!')

        context = {}
        return render(request, 'registration/login.html', context)


def customerLogout(request):
    logout(request)
    return redirect('/')


def customerregister(request):
    form = SignupForm()
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account for ' + user + ' created successfully')
                return redirect('login')

        context = {'form': form}
        return render(request, 'registration/register.html', context)


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/products/list.html', {'category': category,
                                                       'categories': categories, 'products': products})


def product_search(request):
    product = Product.objects.all()
    query = request.GET.get('q')
    if query:
        product = product.filter(
            Q(name__icontains=query) |
            Q(image__icontains=query) |
            Q(slug__icontains=query) |
            Q(available__icontains=query) |
            Q(price__icontains=query)
        )
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form
    }
    return render(request, 'shop/products/search.html', context)




def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    return render(request, 'shop/products/detail.html', {
        'product': product, 'cart_product_form': cart_product_form})
