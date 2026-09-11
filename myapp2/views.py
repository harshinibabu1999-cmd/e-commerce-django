from django.shortcuts import render, redirect
from django.contrib.auth.models import User  
from .forms import ProductForm
from .models import Productdetails, Wishlist
from .models import *
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import cart
from .models import Order
from .models import UserProfile

def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")

        phone = request.POST.get("phone", "")
        address = request.POST.get("address", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")
        country = request.POST.get("country", "")


        # Check username

        if User.objects.filter(username=username).exists():

            return render(
                request,
                "register.html",
                {
                    "error": "Username already exists"
                }
            )


        # Create User

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )


        # Create OR get profile

        profile, created = UserProfile.objects.get_or_create(
            user=user
        )


        # Save profile details

        profile.phone = phone
        profile.address = address
        profile.city = city
        profile.state = state
        profile.country = country

        profile.save()


        # Login

        login(request, user)


        return redirect(
            "myapp2:home"
        )


    return render(
        request,
        "register.html"
    )

        
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('myapp2:admin_dashboard')
                else:
                    return redirect('myapp2:home')
            else:
                form.add_error(None, "Invalid credentials")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def home(request):
    products=product.objects.all()
    return render(request, 'home.html',{'products':products})

def dashboard_login(request):

    if not request.session.get('user_id'):
        return redirect('myapp2:login_view')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username, password=password).first()
        if user:
            if user.role.lower() == "admin":
                return redirect('myapp2:admin_dashboard')
            else:
                return redirect('myapp2:customer_dashboard')
        else:
            return render(request, 'home.html', {'error': 'Invalid credentials'})

    return redirect('myapp2:home')


@login_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_products = Productdetails.objects.count()

    context = {
        'total_users': total_users,
        'total_products': total_products,
    }

    return render(request, 'admin/admin_dashboard.html', context)




def product_list(request):
    products = Productdetails.objects.all()
    return render(request, 'admin/product_list.html', {'products': products})

def admin_add_product(request):
    if request.method == "POST":
        image = request.FILES.get('image')
        product_name = request.POST.get('product_name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        description = request.POST.get('description')

        if image and product_name and quantity and price and description:
            product = Productdetails(
                image=image,
                product_name=product_name,
                quantity=quantity,
                price=price,
                description=description
            )
            product.save()

            return redirect('myapp2:product_list')  

        else:
    
            return render(request, 'admin/admin_add_product.html', {'error': 'All fields are required!'})

    return render(request, 'admin/admin_add_product.html')


def home(request):
    products=Productdetails.objects.all()
    return render(request, 'home.html',{'products':products})

def logout(request):
    request.session.flush()
    return redirect('myapp2:login_view')

@login_required
def delete_product(request, product_id):
    print("Trying to delete product ID:", product_id)

    if not request.user.is_superuser:
        return redirect('myapp2:customer_dashboard')

    product = get_object_or_404(Productdetails, id=product_id)
    product.delete()
    return redirect('myapp2:admin_dashboard')

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Productdetails, id=product_id)

    if request.method == "POST":
        product.product_name = request.POST.get('product_name')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.description = request.POST.get('description')

        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        product.save()
        return redirect('myapp2:product_list')

    return render(request, 'admin/edit_product.html', {'product': product})

def customer_list(request):
    customers = User.objects.filter(is_superuser=False).exclude(last_login=None)
    return render(request, 'Users/customer_list.html', {'customers': customers})

@login_required
def customer_product_list(request):
    products = Productdetails.objects.all()

    wishlist_products = Wishlist.objects.filter(
        user=request.user
    ).values_list('product_id', flat=True)

    context = {
        'products': products,
        'wishlist_products': wishlist_products
    }

    return render(
        request,
        'Users/customer_product_list.html',
        context
    )

@login_required
def wishlist(request, product_id):
    product = Productdetails.objects.get(id=product_id)

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        wishlist_item.delete()

    return redirect('myapp2:customer_product_list')

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'Users/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def buy_product(request, product_id):
    product = get_object_or_404(Productdetails, id=product_id)

    cart_item, created = cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('myapp:checkout')


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Productdetails, id=product_id)

    cart_item, created = cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('myapp2:cart_view')


@login_required
def cart_view(request):
    cart_items = cart.objects.filter(user=request.user)

    total_price = 0

    for item in cart_items:
        item.item_total = item.product.price * item.quantity
        total_price += item.item_total

    return render(request, 'Users/cart_view.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('myapp2:cart_view')

@login_required
def increase_quantity(request, cart_id):
    cart_item = get_object_or_404(cart, id=cart_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('myapp2:cart_view')

@login_required
def decrease_quantity(request, cart_id):
    cart_item = get_object_or_404(cart, id=cart_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('myapp2:cart_view')

@login_required
def checkout(request):
    cart_items = cart.objects.filter(user=request.user)

    total_price = 0
    for item in cart_items:
        total_price += item.product.price * item.quantity

    return render(request, 'Users/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def confirm_payment(request):
    cart_items = cart.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('myapp2:cart_view')

    total_amount = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    if request.method == 'POST':
        for item in cart_items:
            Order.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                total_price=item.product.price * item.quantity,
            )

        messages.success(
            request,
            "Payment successful! Your Order has been placed."
        )

        return redirect('myapp2:payment_successful')

    return render(request, 'Users/confirm_payment.html', {
        'total_amount': total_amount
    })



@login_required
def payment_successful(request):
    return render(request, 'Users/payment_successful.html')

def payment_failed(request):
    return render(request, 'Users/payment_failure.html')

@login_required
def product_view(request, product_id):
    product = get_object_or_404(Productdetails, id=product_id)
    
    orders = Order.objects.filter(product=product).select_related('user')
    context ={
        'product': product,
        'orders': orders

    }
    return render(request, 'admin/product_view.html', context)

@login_required
def order_list(request):
    orders = Order.objects.select_related('user', 'product').all()
    return render(request, 'admin/order_list.html',
     {'orders': orders})


@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).select_related('product').order_by('-order_date')

    return render(request, 'Users/my_orders.html', {
        'orders': orders
    })



@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    return render(request, 'Users/profile.html', {
        'profile': profile
    })

@login_required
def profile_view(request):

    # Admin profile page வேண்டாம்
    if request.user.is_superuser:
        return redirect('myapp:home')

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        'profile.html',
        {
            'user': request.user,
            'profile': profile
        }
    )