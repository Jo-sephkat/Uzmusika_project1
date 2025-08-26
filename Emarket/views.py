import uuid
import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Product,Service, Profile
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlencode
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect




    

def home(request):
    products = Product.objects.all()[:8]
    categories = Product.objects.values_list('category', flat=True).distinct()
    return render(request, 'Emarket/home.html',{'products': products, 'categories': categories})
    
@login_required
def category_products(request, category_name):
    # Filter products by the given category name
    products = Product.objects.filter(category=category_name)
    return render(request, 'Emarket/category_products.html', {'products': products, 'category_name': category_name})

def category_list(request):
    categories = Product.objects.values('category').annotate(count=Count('id')).order_by('category')
    return render(request, 'Emarket/category_list.html', {'categories': categories})

def category_products(request, category_name):
    products = Product.objects.filter(category=category_name)
    return render(request, 'Emarket/category_products.html', {'products': products, 'category_name': category_name})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'Emarket/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'Emarket/product_detail.html', {'product': product})

'''def register(request):
    context={}
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user=User.objects.create_user(username=username,password=password)
        context['success']='User added successfuly'

    return render(request, 'Emarket/index.html', context)'''

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        if User.objects.filter(username=username).exists():
            return render(request, 'Emarket/register.html', {'error': 'Username already exists. Please choose a different one.'})
        
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_active=True                
            )
            
            profile = Profile.objects.create(
                user=user,
                role=role,
                phone=phone,
                address=address,
                is_email_confirmed=True
            )

            try:
                send_mail(
                    'Welcome to UZmarket!',
                    f'Hello {username},\n\nYour account has been created. You can now log in at http://127.0.0.1:8000/signin/\n\nThank you for registering!',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=True,  
                )
                messages.success(request, "Registration successful! A welcome email has been sent.")
            except Exception as e:
                print(f"Email sending error: {e}")
                messages.success(request, "Registration successful! (Email could not be sent)")
            
            return redirect('signin')
            
        except Exception as e:

            print(f"Registration error: {e}")
            return render(request, 'Emarket/register.html', {
                'error': 'An error occurred during registration. Please try again.'
            })
    

    return render(request, 'Emarket/register.html')

def send_mail_page(request):
    context = {}

    if request.method == 'POST':
        address = request.POST.get('address')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if address and subject and message:
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
                context['result'] = 'Email sent successfully'
            except Exception as e:
                context['result'] = f'Error sending email: {e}'
        else:
            context['result'] = 'All fields are required'
    
    return render(request, "signin.html", context)     


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password') 
        user = authenticate(username=username, password=password)
        
        if user is not None:
            try:
                user_profile = Profile.objects.get(user=user)
                '''if not user_profile.is_email_confirmed:
                    messages.error(request, "Please confirm your email before signing in.")
                    return redirect('signin')  # Fixed: using redirect with URL name
                '''
                login(request, user)
                if user_profile.role == 'vendor':
                    return redirect('vendor_dashboard')  # Fixed: using redirect with URL name
                elif user_profile.role == 'buyer':
                    return redirect('buyer_dashboard')  # Fixed: using redirect with URL name
                return redirect('home')  # Fixed: using redirect with URL name
                
            except Profile.DoesNotExist:
                messages.error(request, "Profile not found. Please contact support")
                return redirect('signin')  # Fixed: using redirect with URL name
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('signin')  # Fixed: using redirect with URL name
    
    # GET request or failed POST
    return render(request, 'Emarket/signin.html')



def vendor_dashboard(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'Emarket/vendor_dashboard.html', {'profile': profile})

def buyer_dashboard(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'Emarket/buyer_dashboard.html', {'profile': profile})
                

def about(request):
    return render(request, 'Emarket/about.html')

def contact(request):
    return render(request, 'Emarket/contact.html')

def add_to_cart(request, product_id):
    return redirect('home')
@login_required
def cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    gross_total = 0
    for product in products:
        quantity = cart[str(product.id)]
        total_price = quantity * product.price
        gross_total += total_price
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price,
        })
    return render(request, 'Emarket/cart.html', {
        'cart_items': cart_items,
        'gross_total': gross_total
    })
    
@require_POST
@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 1))
    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str] += quantity
    else:
        cart[product_id_str] = quantity
    request.session['cart'] = cart
    cart_quantity = sum(cart.values())
    if request.headers.get('x-requested-width') == 'XMLHttpRewuest':
        return JsonResponse({'cart_quantity': cart_quantity})
    return redirect('cart')

def cart_quantity(request):
    cart = request.session.get('cart', {})
    quantity = sum(cart.values())
    return {'cart_quantity': quantity}

@login_required
def vendor_profile(request):
    profile = request.user.profile
    user = request.user
    # Add browsing history logic if you have such a model
    # browsing_history = BrowsingHistory.objects.filter(user=user)
    
    return render(request, 'Emarket/vendor_profile.html', {
        'profile': profile,
        'user': user,
        # 'browsing_history'; browsing_history
    })

from django.contrib.auth.decorators import login_required

@login_required
def vendor_edit_profile(request):
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        # Do NOT set user.username unless you have a username field in your form!
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        user.save()
        profile.save()
        return redirect('vendor_profile')
    return render(request, 'Emarket/vendor_edit_profile.html', {'profile': profile, 'user': user})

@login_required
def vendor_products(request):
    profile = request.user.profile
    products = Product.objects.filter(vendor=profile)
    return render(request, 'Emarket/vendor_products.html', {'products': products})

@login_required
def add_product(request):
    profile = request.user.profile
    if  request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        Product.objects.create(
            vendor=profile, name=name, price=price, description=description,category=category, image=image
        )
        return redirect('vendor_products')
    return render(request, 'Emarket/add_product.html')

@login_required
def edit_product(request, pk):
    profile = request.user.profile
    product = get_object_or_404(Product, pk=pk, vendor=profile)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.category = request.POST.get('category')
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        product.save()
        return redirect('vendor_products')
    return render(request, 'Emarket/edit_product.html', {'product': product})

@login_required
def delete_product(request, pk):
    profile = request.user.profile
    product = get_object_or_404(Product, pk=pk, vendor=profile)
    product.delete()
    return redirect('vendor_products')

from django.views.decorators.http import require_POST

@require_POST
def update_cart_item(request, product_id):
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 1))
    product_id_str = str(product_id)
    if quantity > 0:
        cart[product_id_str] = quantity
    else:
        cart.pop(product_id_str, None)
    request.session['cart'] = cart
    return redirect('cart')

@require_POST
def remove_cart_item(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    cart.pop(product_id_str, None)
    request.session['cart'] = cart
    return redirect('cart')

@login_required
def buyer_profile(request):
    profile = request.user.profile
    user = request.user
    return render(request, 'Emarket/buyer_profile.html', {'profile': profile, 'user': user})

@login_required
def buyer_edit_profile(request):
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        user.save()
        profile.save()
        return redirect('buyer_profile')
    return render(request, 'Emarket/buyer_edit_profile.html', {'profile': profile, 'user': user})

@login_required
def make_purchase(request):
    # Implement your purchase logic here (e.g., create Order, clear cart)
    # For now, just clear the cart and show a success message
    request.session['cart'] = {}
    return render(request, 'Emarket/purchase_success.html')


stripe.api_key = settings.STRIPE_SECRET_KEY

def make_purchase(request):
    # Your existing purchase logic
    context = {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'order_total': 1000,  # Calculate this from cart
    }
    return render(request, 'Emarket/make_purchase.html', context)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Your Order',
                            },
                            'unit_amount': int(request.POST.get('amount')) * 100,
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri('/payment-success/'),
                cancel_url=request.build_absolute_uri('/payment-cancelled/'),
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return HttpResponse(status=400)


def payment_success(request):
    return render(request, 'Emarket/payment_success.html')

def payment_cancelled(request):
    return render(request, 'Emarket/payment_cancelled.html')




def test_email(request):
    send_mail(
        'Test Email',
        'This is a test email from Django.',
        settings.DEFAULT_FROM_EMAIL,
        ['recipient@example.com'],  # Replace with your email
        fail_silently=False,
    )
    return HttpResponse("Test email sent!")

def help_center(request):
    return render(request, 'Emarket/help_center.html')

def privacy_policy(request):
    return render(request, 'Emarket/privacy_policy.html')

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Send email (configure SMTP in settings.py)
        send_mail(
            f"Contact Form: {name}",
            message,
            email,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        messages.success(request, "Your message has been sent!")
        return HttpResponseRedirect('/contact-us/')
    return render(request, 'Emarket/contact_us.html')

def feedback(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        # Save to DB or send email
        messages.success(request, "Thank you for your feedback!")
        return HttpResponseRedirect('/feedback/')
    return render(request, 'Emarket/feedback.html')
