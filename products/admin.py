# products/admin.py

from django.contrib import admin
from .models import CustomUser, Product, CartItem

admin.site.register(Product)
