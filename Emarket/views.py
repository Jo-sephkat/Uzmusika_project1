import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Product, Service, Profile, Order, OrderItem, UNIVERSITIES, CATEGORIES, CONDITIONS, PAYMENT_CHOICES, CATEGORY_ICONS
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Count, Q, Sum
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings


def home(request):
    products = Product.objects.filter(is_available=True).select_related('vendor', 'vendor__user').order_by('-date_added')
    recent_products = products[:8]
    
    # Categories with count and icon
    category_data = []
    for cat_name, _ in CATEGORIES:
        count = Product.objects.filter(category=cat_name, is_available=True).count()
        icon = CATEGORY_ICONS.get(cat_name, '📦')
        category_data.append({
            'name': cat_name,
            'icon': icon,
            'count': count
        })
    
    unis = [u[0] for u in UNIVERSITIES]
    total_listings = products.count()
    total_unis = len(unis)
    total_payment_methods = len(PAYMENT_CHOICES)

    return render(request, 'Emarket/home.html', {
        'products': recent_products,
        'category_data': category_data,
        'universities': unis,
        'total_listings': total_listings,
        'total_unis': total_unis,
        'total_payment_methods': total_payment_methods,
    })


def product_list(request):
    search_query = request.GET.get('search', '').strip()
    category_query = request.GET.get('cat', '').strip() or request.GET.get('category', '').strip()
    uni_query = request.GET.get('uni', '').strip() or request.GET.get('university', '').strip()
    
    products = Product.objects.filter(is_available=True).select_related('vendor', 'vendor__user').order_by('-date_added')
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(university__icontains=search_query) |
            Q(vendor__store_name__icontains=search_query)
        )
    if category_query:
        products = products.filter(category__iexact=category_query)
    if uni_query:
        products = products.filter(
            Q(university__iexact=uni_query) |
            Q(vendor__university__iexact=uni_query)
        )

    unis = [u[0] for u in UNIVERSITIES]
    category_data = [
        {'name': c[0], 'icon': CATEGORY_ICONS.get(c[0], '📦')}
        for c in CATEGORIES
    ]

    return render(request, 'Emarket/product_list.html', {
        'products': products,
        'search_query': search_query,
        'selected_category': category_query,
        'selected_uni': uni_query,
        'category_data': category_data,
        'universities': unis,
        'total_count': products.count()
    })


def category_list(request):
    category_data = []
    for cat_name, _ in CATEGORIES:
        count = Product.objects.filter(category=cat_name, is_available=True).count()
        icon = CATEGORY_ICONS.get(cat_name, '📦')
        category_data.append({
            'name': cat_name,
            'icon': icon,
            'count': count
        })
    return render(request, 'Emarket/category_list.html', {'categories': category_data})


def category_products(request, category_name):
    products = Product.objects.filter(category__iexact=category_name, is_available=True).select_related('vendor', 'vendor__user').order_by('-date_added')
    icon = CATEGORY_ICONS.get(category_name, '📦')
    return render(request, 'Emarket/category_products.html', {
        'products': products,
        'category_name': category_name,
        'category_icon': icon,
        'total_count': products.count()
    })


def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related('vendor', 'vendor__user'), pk=pk)
    related_products = Product.objects.filter(
        category=product.category, is_available=True
    ).exclude(pk=pk).select_related('vendor', 'vendor__user')[:4]
    return render(request, 'Emarket/product_detail.html', {
        'product': product,
        'related_products': related_products
    })


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        role = request.POST.get('role', 'buyer')
        university = request.POST.get('university', 'University of Zimbabwe')
        phone = request.POST.get('phone', '').strip()
        store_name = request.POST.get('store_name', '').strip()

        if not username or not password:
            return render(request, 'Emarket/register.html', {
                'error': 'Username and password are required.',
                'universities': [u[0] for u in UNIVERSITIES]
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'Emarket/register.html', {
                'error': 'Username already taken. Please choose another username.',
                'universities': [u[0] for u in UNIVERSITIES]
            })

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_active=True
            )
            
            Profile.objects.create(
                user=user,
                role=role,
                university=university,
                store_name=store_name,
                phone=phone,
                is_email_confirmed=True
            )

            # Auto log in user
            login(request, user)
            messages.success(request, f"Welcome to UniTrade, {username}!")
            if role == 'vendor':
                return redirect('vendor_dashboard')
            return redirect('home')

        except Exception as e:
            return render(request, 'Emarket/register.html', {
                'error': f'Registration error: {str(e)}',
                'universities': [u[0] for u in UNIVERSITIES]
            })

    return render(request, 'Emarket/register.html', {
        'universities': [u[0] for u in UNIVERSITIES]
    })


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip() 
        user = authenticate(username=username, password=password)
        
        if user is not None:
            profile, _ = Profile.objects.get_or_create(user=user, defaults={'role': 'buyer'})
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            if profile.role == 'vendor':
                return redirect('vendor_dashboard')
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'Emarket/signin.html', {'error': 'Invalid username or password.'})
    
    return render(request, 'Emarket/signin.html')


@login_required
def vendor_dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user, defaults={'role': 'vendor'})
    products = Product.objects.filter(vendor=profile).order_by('-date_added')
    total_products = products.count()
    total_value = sum(p.price for p in products)

    # All order items for this vendor's products
    all_vendor_items = OrderItem.objects.filter(product__vendor=profile).select_related('order', 'product', 'order__buyer')
    vendor_order_items = all_vendor_items.order_by('-order__date_ordered')[:20]

    # Financial summary
    confirmed_items = all_vendor_items.filter(order__status='Confirmed')
    completed_items = all_vendor_items.filter(order__status='Completed')
    pending_items   = all_vendor_items.filter(order__status='Pending')
    cancelled_items = all_vendor_items.filter(order__status='Cancelled')

    revenue_confirmed  = sum(i.total_price for i in confirmed_items)
    revenue_completed  = sum(i.total_price for i in completed_items)
    revenue_pending    = sum(i.total_price for i in pending_items)
    revenue_cancelled  = sum(i.total_price for i in cancelled_items)
    total_sales_revenue = revenue_confirmed + revenue_completed
    total_sales_count   = confirmed_items.values('order').distinct().count() + completed_items.values('order').distinct().count()
    pending_orders_count = pending_items.values('order').distinct().count()

    return render(request, 'Emarket/vendor_dashboard.html', {
        'profile': profile,
        'products': products,
        'total_products': total_products,
        'total_value': total_value,
        'total_sales_revenue': total_sales_revenue,
        'vendor_order_items': vendor_order_items,
        'recent_products': products[:5],
        # financials
        'revenue_confirmed': revenue_confirmed,
        'revenue_completed': revenue_completed,
        'revenue_pending': revenue_pending,
        'revenue_cancelled': revenue_cancelled,
        'total_sales_count': total_sales_count,
        'pending_orders_count': pending_orders_count,
    })


@login_required
def vendor_revenue(request):
    """Dedicated Revenue & Sales Analytics page with Revenue Summary, Order Pipeline, and Sales Performance."""
    profile, _ = Profile.objects.get_or_create(user=request.user, defaults={'role': 'vendor'})
    products = Product.objects.filter(vendor=profile).order_by('-date_added')
    total_products = products.count()
    total_value = sum(p.price for p in products)

    all_vendor_items = OrderItem.objects.filter(product__vendor=profile).select_related('order', 'product', 'order__buyer')
    vendor_order_items = all_vendor_items.order_by('-order__date_ordered')

    confirmed_items = all_vendor_items.filter(order__status='Confirmed')
    completed_items = all_vendor_items.filter(order__status='Completed')
    pending_items   = all_vendor_items.filter(order__status='Pending')
    cancelled_items = all_vendor_items.filter(order__status='Cancelled')

    revenue_confirmed  = sum(i.total_price for i in confirmed_items)
    revenue_completed  = sum(i.total_price for i in completed_items)
    revenue_pending    = sum(i.total_price for i in pending_items)
    revenue_cancelled  = sum(i.total_price for i in cancelled_items)
    total_sales_revenue = revenue_confirmed + revenue_completed
    total_sales_count   = confirmed_items.values('order').distinct().count() + completed_items.values('order').distinct().count()
    pending_orders_count = pending_items.values('order').distinct().count()

    tab = request.GET.get('tab', 'summary')
    if tab not in ['summary', 'pipeline', 'performance']:
        tab = 'summary'

    return render(request, 'Emarket/vendor_revenue.html', {
        'profile': profile,
        'tab': tab,
        'products': products,
        'total_products': total_products,
        'total_value': total_value,
        'total_sales_revenue': total_sales_revenue,
        'vendor_order_items': vendor_order_items,
        'revenue_confirmed': revenue_confirmed,
        'revenue_completed': revenue_completed,
        'revenue_pending': revenue_pending,
        'revenue_cancelled': revenue_cancelled,
        'total_sales_count': total_sales_count,
        'pending_orders_count': pending_orders_count,
        'confirmed_items': confirmed_items,
        'completed_items': completed_items,
        'pending_items': pending_items,
        'cancelled_items': cancelled_items,
    })


@login_required
def buyer_dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user, defaults={'role': 'buyer'})
    orders = Order.objects.filter(buyer=request.user).prefetch_related('items__product').order_by('-date_ordered')
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    return render(request, 'Emarket/buyer_dashboard.html', {
        'profile': profile,
        'orders': orders,
        'orders_count': orders.count(),
        'cart_count': cart_count
    })


@require_POST
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 1))
    product_id_str = str(product_id)
    
    product = get_object_or_404(Product, pk=product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + max(1, quantity)
    request.session['cart'] = cart
    cart_quantity = sum(cart.values())
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax') == '1':
        return JsonResponse({
            'success': True,
            'message': f"Added '{product.name}' to cart",
            'cart_quantity': cart_quantity
        })
    
    messages.success(request, f"'{product.name}' added to cart.")
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'cart'
    return redirect(next_url)


def cart(request):
    cart = request.session.get('cart', {})
    product_ids = [int(k) for k in cart.keys() if cart[k] > 0]
    products = Product.objects.filter(id__in=product_ids).select_related('vendor')
    
    cart_items = []
    gross_total = 0
    for product in products:
        qty = cart.get(str(product.id), 0)
        if qty > 0:
            total_price = qty * product.price
            gross_total += total_price
            cart_items.append({
                'product': product,
                'quantity': qty,
                'total_price': total_price,
            })
            
    return render(request, 'Emarket/cart.html', {
        'cart_items': cart_items,
        'gross_total': gross_total,
        'total_items_count': sum(cart.values())
    })


@require_POST
def update_cart_item(request, product_id):
    cart = request.session.get('cart', {})
    change = int(request.POST.get('change', 0))
    set_qty = request.POST.get('quantity')
    product_id_str = str(product_id)
    
    if set_qty is not None:
        new_qty = int(set_qty)
    else:
        new_qty = cart.get(product_id_str, 1) + change

    if new_qty <= 0:
        cart.pop(product_id_str, None)
        messages.info(request, "Item removed from cart.")
    else:
        cart[product_id_str] = new_qty

    request.session['cart'] = cart
    return redirect('cart')


@require_POST
def remove_cart_item(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    cart.pop(product_id_str, None)
    request.session['cart'] = cart
    messages.info(request, "Item removed from cart.")
    return redirect('cart')


def make_purchase(request):
    cart = request.session.get('cart', {})
    product_ids = [int(k) for k in cart.keys() if cart[k] > 0]
    if not product_ids:
        messages.info(request, "Your cart is empty. Explore our campus marketplace!")
        return redirect('product_list')

    products = Product.objects.filter(id__in=product_ids).select_related('vendor')
    cart_items = []
    order_total = 0
    for product in products:
        qty = cart.get(str(product.id), 0)
        if qty > 0:
            item_total = qty * product.price
            order_total += item_total
            cart_items.append({
                'product': product,
                'quantity': qty,
                'total_price': item_total,
            })

    # Payment rail descriptors
    payment_options = [
        {
            'id': 'ecocash',
            'name': 'EcoCash',
            'tag': 'Most used',
            'note': "Pay from your EcoCash USD wallet — you'll arrange transfer or prompt with seller.",
        },
        {
            'id': 'innbucks',
            'name': 'InnBucks',
            'tag': 'Instant',
            'note': 'Settle in the InnBucks app or generate voucher code for quick handover.',
        },
        {
            'id': 'onemoney',
            'name': 'OneMoney',
            'tag': 'NetOne',
            'note': 'Direct mobile money transfer for NetOne subscribers.',
        },
        {
            'id': 'zipit',
            'name': 'ZIPIT / Bank transfer',
            'tag': 'Bank',
            'note': 'Instant bank-to-bank transfer from any Zimbabwean bank account.',
        },
        {
            'id': 'cash',
            'name': 'Cash on campus',
            'tag': 'Meet-up',
            'note': 'Hand over physical cash directly to the student seller upon meeting.',
        },
    ]

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'ecocash')
        payment_number = request.POST.get('payment_number', '').strip()
        buyer_name = request.POST.get('buyer_name', '').strip()
        buyer_contact = request.POST.get('buyer_contact', '').strip()

        # If user is logged in use user, otherwise create/get guest account
        if request.user.is_authenticated:
            buyer_user = request.user
        else:
            # Create/Find guest buyer
            guest_email = buyer_contact if '@' in buyer_contact else f"guest_{uuid.uuid4().hex[:6]}@campus.unitrade.zw"
            guest_username = f"buyer_{uuid.uuid4().hex[:8]}"
            buyer_user = User.objects.create_user(
                username=guest_username,
                email=guest_email,
                first_name=buyer_name or "Campus Student",
                is_active=True
            )
            Profile.objects.create(
                user=buyer_user,
                role='buyer',
                phone=payment_number or buyer_contact
            )

        # Create Order
        order = Order.objects.create(
            buyer=buyer_user,
            total_amount=order_total,
            payment_method=payment_method,
            payment_number=payment_number or buyer_contact,
            status='Pending'
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )

        # Clear cart
        request.session['cart'] = {}
        return render(request, 'Emarket/purchase_success.html', {
            'order': order,
            'cart_items': cart_items,
            'order_total': order_total
        })

    return render(request, 'Emarket/make_purchase.html', {
        'order_total': order_total,
        'cart_items': cart_items,
        'payment_options': payment_options
    })


@login_required
def add_product(request):
    profile, _ = Profile.objects.get_or_create(user=request.user, defaults={'role': 'vendor'})
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        price = request.POST.get('price', 0)
        description = request.POST.get('description', '').strip()
        category = request.POST.get('category', 'Textbooks')
        condition = request.POST.get('condition', 'Used')
        university = request.POST.get('university') or profile.university
        icon = request.POST.get('icon', CATEGORY_ICONS.get(category, '📦'))
        image = request.FILES.get('image')

        if name and price:
            Product.objects.create(
                vendor=profile,
                name=name,
                price=price,
                description=description,
                category=category,
                condition=condition,
                university=university,
                icon=icon,
                image=image,
                is_available=True
            )
            profile.role = 'vendor'
            profile.save()
            messages.success(request, f"'{name}' listed on UniTrade marketplace!")
            return redirect('vendor_dashboard')

    return render(request, 'Emarket/add_product.html', {
        'categories': [c[0] for c in CATEGORIES],
        'conditions': [c[0] for c in CONDITIONS],
        'universities': [u[0] for u in UNIVERSITIES],
        'category_icons': CATEGORY_ICONS,
        'profile': profile
    })


@login_required
def edit_product(request, pk):
    profile = request.user.profile
    product = get_object_or_404(Product, pk=pk, vendor=profile)
    if request.method == 'POST':
        product.name = request.POST.get('name', product.name)
        product.price = request.POST.get('price', product.price)
        product.description = request.POST.get('description', product.description)
        product.category = request.POST.get('category', product.category)
        product.condition = request.POST.get('condition', product.condition)
        product.university = request.POST.get('university', product.university)
        product.icon = request.POST.get('icon', product.icon)
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        product.save()
        messages.success(request, f"'{product.name}' updated successfully.")
        return redirect('vendor_dashboard')

    return render(request, 'Emarket/edit_product.html', {
        'product': product,
        'categories': [c[0] for c in CATEGORIES],
        'conditions': [c[0] for c in CONDITIONS],
        'universities': [u[0] for u in UNIVERSITIES],
    })


@login_required
def delete_product(request, pk):
    profile = request.user.profile
    product = get_object_or_404(Product, pk=pk, vendor=profile)
    p_name = product.name
    product.delete()
    messages.info(request, f"'{p_name}' has been removed from your store.")
    return redirect('vendor_dashboard')


@login_required
@require_POST
def update_order_status(request, order_id):
    """Allow a vendor to update the status of an order that contains their product(s)."""
    profile, _ = Profile.objects.get_or_create(user=request.user, defaults={'role': 'vendor'})
    order = get_object_or_404(Order, pk=order_id)

    # Verify this vendor owns at least one item in the order
    owns_item = OrderItem.objects.filter(order=order, product__vendor=profile).exists()
    if not owns_item:
        messages.error(request, "You don't have permission to update this order.")
        return redirect('vendor_dashboard')

    new_status = request.POST.get('status', '').strip()
    allowed = ['Confirmed', 'Completed', 'Cancelled']
    if new_status not in allowed:
        messages.error(request, "Invalid status.")
        return redirect('vendor_dashboard')

    order.status = new_status
    order.save()
    messages.success(request, f"Order {order.order_reference} marked as '{new_status}'.")
    return redirect('vendor_dashboard')


@login_required
def profile_view(request):
    """Unified Profile & Account view that cleanly differentiates User Details, Settings, Dashboard, and Session."""
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    tab = request.GET.get('tab')
    if not tab:
        if 'edit' in request.path or 'settings' in request.path:
            tab = 'settings'
        else:
            tab = 'details'

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name).strip()
        user.last_name = request.POST.get('last_name', user.last_name).strip()
        user.email = request.POST.get('email', user.email).strip()

        if profile.role == 'vendor' or request.POST.get('store_name'):
            profile.store_name = request.POST.get('store_name', profile.store_name).strip()

        profile.university = request.POST.get('university', profile.university)
        profile.phone = request.POST.get('phone', profile.phone).strip()
        profile.address = request.POST.get('address', profile.address).strip()

        # Optional password update
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        if new_password:
            if new_password == confirm_password:
                user.set_password(new_password)
                login(request, user)
                messages.success(request, "Account settings and password updated successfully!")
            else:
                messages.error(request, "Passwords did not match. Other changes were saved.")
        else:
            messages.success(request, "Profile and account details updated successfully.")

        user.save()
        profile.save()
        return redirect(f"{request.path}?tab=settings")

    products_count = 0
    sales_count = 0
    total_revenue = 0
    orders_count = 0
    cart_count = 0

    if profile.role == 'vendor':
        products = Product.objects.filter(vendor=profile)
        products_count = products.count()
        vendor_items = OrderItem.objects.filter(product__vendor=profile)
        completed_items = vendor_items.filter(order__status__in=['Confirmed', 'Completed'])
        sales_count = completed_items.values('order').distinct().count()
        total_revenue = sum(i.total_price for i in completed_items)
    else:
        orders_count = Order.objects.filter(buyer=user).count()
        cart = request.session.get('cart', {})
        cart_count = sum(cart.values())

    return render(request, 'Emarket/profile.html', {
        'profile': profile,
        'user': user,
        'tab': tab,
        'products_count': products_count,
        'sales_count': sales_count,
        'total_revenue': total_revenue,
        'orders_count': orders_count,
        'cart_count': cart_count,
        'universities': [u[0] for u in UNIVERSITIES],
    })


@login_required
def vendor_products(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    products = Product.objects.filter(vendor=profile).order_by('-date_added')
    return render(request, 'Emarket/vendor_products.html', {'products': products})


# Unify Account and Profile: all routes point to the unified profile view
vendor_profile = profile_view
buyer_profile = profile_view
account_settings = profile_view
vendor_edit_profile = profile_view
buyer_edit_profile = profile_view


def about(request):
    unis = [u[0] for u in UNIVERSITIES]
    return render(request, 'Emarket/about.html', {
        'universities': unis,
        'payment_methods': [p[1] for p in PAYMENT_CHOICES]
    })


def contact(request):
    return render(request, 'Emarket/contact.html')


def contact_us(request):
    if request.method == 'POST':
        messages.success(request, "Thank you! Your message has been sent to the UniTrade campus team.")
        return redirect('contact_us')
    return render(request, 'Emarket/contact_us.html')


def help_center(request):
    return render(request, 'Emarket/help_center.html')


def privacy_policy(request):
    return render(request, 'Emarket/privacy_policy.html')


def feedback(request):
    if request.method == 'POST':
        messages.success(request, "Thank you for your feedback! It helps us improve UniTrade.")
        return redirect('feedback')
    return render(request, 'Emarket/feedback.html')
