# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import uuid

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    registration_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Store"

'''class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='productimages/', blank=True, null=True)
    
    def __str__(self):
        return self.name
'''
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_info = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    registration_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}" if hasattr(self, 'user') else f"Student {self.iid}"
    
    
class Profile(models.Model):
    ROLE_CHOICES = [
        ('vendor', 'vendor'),
        ('buyer', 'buyer')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_email_confirmed = models.BooleanField(default=False)
    email_confirmation_token = models.UUIDField(default=uuid.uuid4)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    pass

class Product(models.Model):
    vendor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    description = models.TextField()
    category = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    
class Service(models.Model):
    vendor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    
    
    
