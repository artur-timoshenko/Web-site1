from django.contrib import admin
from .models import CartItem, Product, PaymentSession, OrderItem, Customer

admin.site.register(CartItem)
admin.site.register(Product)
admin.site.register(PaymentSession)
admin.site.register(OrderItem)
admin.site.register(Customer)
