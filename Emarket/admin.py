# Register your models here.
from django.contrib import admin
from .models import Vendor, Product, Student

admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(Student)



