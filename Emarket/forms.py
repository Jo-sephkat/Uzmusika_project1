from django import forms
from .models import Product
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm



     
    

class ProductForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = ['name', 'description', 'price', 'vendor', 'category', 'image']  # Add other fields as needed
    
