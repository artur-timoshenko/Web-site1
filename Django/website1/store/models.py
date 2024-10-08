from django.db import models
from django.contrib.auth.models import User


# class User(models.Model):
#     username = models.CharField("Username", max_length=240)
#     password = models.CharField("Password", max_length=240)
#     email = models.EmailField()
#     phone = models.CharField(max_length=20)
#     registrationDate = models.DateField("Registration Date", auto_now_add=True)
#     photo = models.CharField("URL", max_length=512)
#
#     def __str__(self):
#         return self.username


class Product(models.Model):
    title = models.CharField("Title", max_length=240)
    description = models.CharField("Description", max_length=240)
    price = models.DecimalField("Price", decimal_places=2, max_digits=9, default=0)
    photo = models.ImageField("Image", upload_to="products/")

    def __str__(self):
        return self.title


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customerID = models.CharField("CustomerID", max_length=240)


class PaymentIntent(models.Model):
    status = models.CharField("Status", default='pending', max_length=240)
    amount = models.DecimalField("Amount", decimal_places=2, max_digits=9, default=0)
    intent = models.CharField("Intent", max_length=240)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class CartItem(models.Model):
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    paymentIntent = models.ForeignKey(PaymentIntent, on_delete=models.CASCADE, null=True, blank=True)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    paymentIntent = models.ForeignKey(PaymentIntent, on_delete=models.CASCADE, null=True, blank=True)
