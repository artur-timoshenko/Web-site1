from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField("Title", max_length=240)
    description = models.CharField("Description", max_length=240)
    price = models.DecimalField("Price", decimal_places=2, max_digits=9, default=0)
    photo = models.ImageField("Image", upload_to="products/")
    new = models.BooleanField("New", default=False)
    salePercent = models.DecimalField("Sale percent", decimal_places=0, max_digits=2, default=0)
    season = models.BooleanField("Season", default=False)

    def __str__(self):
        return self.title

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="store4Customer")
    customerID = models.CharField("CustomerID", max_length=240)
    clientSecret = models.CharField("clientSecret", max_length=240, null=True, blank=True)
    expiresAt = models.IntegerField("ExpiresAt", null=True, blank=True)


# class PaymentIntent(models.Model):
#     status = models.CharField("Status", default='pending', max_length=240)
#     amount = models.DecimalField("Amount", decimal_places=2, max_digits=9, default=0)
#     intent = models.CharField("Intent", max_length=240)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="store3Customer")


class PaymentSession(models.Model):
    status = models.CharField("Status", default='pending', max_length=240)
    amountTotal = models.DecimalField("Amount total", decimal_places=2, max_digits=9, default=0)
    session = models.CharField("Session", max_length=240)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="store4Customer")


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="store4UserCartItem")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    # paymentIntent = models.ForeignKey(PaymentIntent, on_delete=models.CASCADE, null=True, blank=True)
    paymentSession = models.ForeignKey(PaymentSession, on_delete=models.CASCADE, null=True, blank=True)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="store4UserOrderItem")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    # paymentIntent = models.ForeignKey(PaymentIntent, on_delete=models.CASCADE)
    paymentSession = models.ForeignKey(PaymentSession, on_delete=models.CASCADE, null=True, blank=True)
