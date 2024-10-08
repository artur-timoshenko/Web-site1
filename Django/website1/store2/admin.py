from django.contrib import admin
from .models import Banner, CartItem, Product, PaymentIntent, OrderItem, Customer

admin.site.register(Banner)
admin.site.register(CartItem)
admin.site.register(Product)
admin.site.register(PaymentIntent)
admin.site.register(OrderItem)
admin.site.register(Customer)
