from django.contrib import admin
from .models import Product, CartItem, PaymentIntent, OrderItem, Customer

# from django.contrib.auth.models import User

# admin.site.register(User)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(PaymentIntent)
admin.site.register(OrderItem)
admin.site.register(Customer)
