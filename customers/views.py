from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Customer, Order, OrderItem
from .forms import CustomerRegistrationForm, CustomerLoginForm, CheckoutForm
from menu.models import MenuItem

def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to OrderKanto!')
            return redirect('customers:cart')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = CustomerRegistrationForm()
    
    return render(request, 'customers/register.html', {'form': form})

def customer_login(request):
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('customers:cart')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomerLoginForm()
    
    return render(request, 'customers/login.html', {'form': form})

def customer_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def cart(request):
    try:
        customer = Customer.objects.get(user=request.user)
        # Get or create a pending order for the customer
        order, created = Order.objects.get_or_create(
            customer=customer,
            status='pending',
            defaults={'delivery_address': customer.address}
        )
        cart_items = order.items.all()
        total_price = order.total_price
    except Customer.DoesNotExist:
        cart_items = []
        total_price = 0
        order = None
    
    return render(request, 'customers/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'order': order
    })

@login_required
@require_POST
def add_to_cart(request):
    try:
        customer = Customer.objects.get(user=request.user)
        menu_item_id = request.POST.get('menu_item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            return JsonResponse({'success': False, 'message': 'Quantity must be positive'})
        
        menu_item = get_object_or_404(MenuItem, id=menu_item_id)
        
        # Get or create a pending order
        order, created = Order.objects.get_or_create(
            customer=customer,
            status='pending'
        )
        
        # Check if item already exists in cart
        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            menu_item=menu_item,
            defaults={'quantity': quantity}
        )
        
        if not created:
            order_item.quantity += quantity
            order_item.save()
        
        messages.success(request, f'{quantity} {menu_item.name}(s) added to cart!')
        return JsonResponse({'success': True, 'message': 'Item added to cart'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
@require_POST
def update_cart_item(request, item_id):
    try:
        order_item = get_object_or_404(OrderItem, id=item_id)
        
        # Check if the order item belongs to the current user
        if order_item.order.customer.user != request.user:
            return JsonResponse({'success': False, 'message': 'Unauthorized'})
        
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            order_item.delete()
            messages.success(request, 'Item removed from cart')
        else:
            order_item.quantity = quantity
            order_item.save()
            messages.success(request, 'Cart updated successfully')
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
@require_POST
def remove_from_cart(request, item_id):
    try:
        order_item = get_object_or_404(OrderItem, id=item_id)
        
        # Check if the order item belongs to the current user
        if order_item.order.customer.user != request.user:
            return JsonResponse({'success': False, 'message': 'Unauthorized'})
        
        item_name = order_item.menu_item.name
        order_item.delete()
        messages.success(request, f'{item_name} removed from cart')
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
def checkout(request):
    try:
        customer = Customer.objects.get(user=request.user)
        order = get_object_or_404(Order, customer=customer, status='pending')
        
        if not order.items.exists():
            messages.warning(request, 'Your cart is empty. Please add items before checkout.')
            return redirect('customers:cart')
        
        if request.method == 'POST':
            form = CheckoutForm(request.POST, instance=order)
            if form.is_valid():
                order = form.save()
                order.status = 'confirmed'
                order.save()
                messages.success(request, 'Order confirmed successfully! We will contact you soon.')
                return redirect('customers:order_confirmation', order_id=order.id)
        else:
            form = CheckoutForm(instance=order)
        
        return render(request, 'customers/checkout.html', {
            'form': form,
            'order': order
        })
        
    except Customer.DoesNotExist:
        messages.error(request, 'Customer profile not found.')
        return redirect('customers:register')
    except Order.DoesNotExist:
        messages.warning(request, 'No pending order found.')
        return redirect('customers:cart')

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer__user=request.user)
    return render(request, 'customers/order_confirmation.html', {'order': order})

@login_required
def order_history(request):
    try:
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).exclude(status='pending').order_by('-created_at')
        return render(request, 'customers/order_history.html', {'orders': orders})
    except Customer.DoesNotExist:
        messages.error(request, 'Customer profile not found.')
        return redirect('customers:register')

# Legacy view - keeping for backward compatibility
def order(request):
    if request.user.is_authenticated:
        return redirect('customers:cart')
    else:
        messages.info(request, 'Please log in to view your cart.')
        return redirect('customers:customer_login')