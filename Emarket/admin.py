from django.contrib import admin
from .models import Profile, Product, Service, Order, OrderItem

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'university', 'phone', 'is_email_confirmed')
    list_filter = ('role', 'university', 'is_email_confirmed')
    search_fields = ('user__username', 'user__email', 'phone', 'store_name')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'category', 'price', 'condition', 'university', 'is_available', 'date_added')
    list_filter = ('category', 'condition', 'university', 'is_available')
    search_fields = ('name', 'description', 'vendor__user__username')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'price', 'category', 'date_added')
    list_filter = ('category',)
    search_fields = ('name', 'description')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_reference', 'buyer', 'total_amount', 'payment_method', 'status', 'date_ordered')
    list_filter = ('status', 'payment_method', 'date_ordered')
    search_fields = ('order_reference', 'buyer__username', 'payment_number')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
