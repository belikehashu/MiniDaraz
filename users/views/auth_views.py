from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from brandpanel.models.owner import Owner
from cart.services.get_user_cart import get_user_cart
from managerpanel.models.manager import Manager
from users.forms import RegisterForm
from products.models.product import Product
from cart.models.cart_item import CartItem

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            if user.is_superuser:
                messages.error(request, "Superuser login not allowed.")
                return redirect('login')

            login(request, user)

            # ✅ Get user's cart from DB
            user_cart = get_user_cart(user=user, session=request.session)

            # ✅ Merge guest cart from SESSION
            session_guest_cart = request.session.get("guest_cart", [])

            for entry in session_guest_cart:
                product_id = entry["product_id"]
                quantity = entry["quantity"]
                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    continue

                cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)
                if not created:
                    cart_item.quantity += quantity
                else:
                    cart_item.quantity = quantity
                cart_item.save()

            # ✅ Clean up guest cart session
            request.session.pop("guest_cart", None)
            request.session.pop("guest_cart_id", None)

            if user.role in ['owner', 'manager']:
                logout(request)
                messages.error(request, "User does not exist.")
                return redirect('login')

            return redirect('profile')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
