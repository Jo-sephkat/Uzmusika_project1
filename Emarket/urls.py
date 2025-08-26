from django.urls import path, reverse_lazy
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_list, name='add_product'),
   
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('about/', views.about, name='about'), 
    path('register/', views.register, name='register') ,  
    path('signin/', views.signin, name='signin'),
    path('home/', views.home, name='home'), 
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('category/<str:category_name>/', views.category_products, name='category_products'),
    path('cart/', views.cart, name='cart'),
    path('vendor-dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('buyer-dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('vendor/profile/', views.vendor_profile, name='vendor_profile'),
    path('vendor/profile/edit/', views.vendor_edit_profile, name='vendor_edit_profile'),
    path('vendor/products/', views.vendor_products, name='vendor_products'),
    path('vendor/products/add/', views.add_product, name='add_product'),
    path('vendor/products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('vendor/products/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('cart/update/<int:product_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('category/', views.category_list, name='category_list'),
    path('category/<str:category_name>/', views.category_products, name='category_products'),
    path('buyer/profile/', views.buyer_profile, name='buyer_profile'),
    path('buyer/profile/edit/', views.buyer_edit_profile, name='buyer_edit_profile'),
    path('make-purchase/', views.make_purchase, name='make_purchase'),
    path('logout/', auth_views.LogoutView.as_view(next_page='signin'), name='logout'),
    path('', views.send_mail_page),  # Added missing comma here
    path('password-reset/',
            auth_views.PasswordResetView.as_view(
                template_name='Emarket/password_reset.html',
                email_template_name='Emarket/password_reset_email.html',
                subject_template_name='Emarket/password_reset_subject.txt',
                success_url=reverse_lazy('password_reset_done')
            ),
            name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='Emarket/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='Emarket/password_reset_confirm.html',
             success_url=reverse_lazy('password_reset_complete')
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='Emarket/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('make-purchase/', views.make_purchase, name='make_purchase'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('help-center/', views.help_center, name='help_center'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('feedback/', views.feedback, name='feedback'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
