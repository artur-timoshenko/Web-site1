# Generated by Django 4.2.15 on 2024-10-06 16:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Banner', max_length=240, verbose_name='Title')),
                ('description', models.CharField(blank=True, max_length=240, null=True, verbose_name='Description')),
                ('link', models.URLField(blank=True, null=True, verbose_name='Link')),
                ('photo', models.ImageField(upload_to='banners/', verbose_name='Image')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customerID', models.CharField(max_length=240, verbose_name='CustomerID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store2Customer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=240, verbose_name='Title')),
                ('description', models.CharField(max_length=240, verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Price')),
                ('photo', models.ImageField(upload_to='products/', verbose_name='Image')),
                ('new', models.BooleanField(default=False, verbose_name='New')),
                ('salePercent', models.DecimalField(decimal_places=0, default=0, max_digits=2, verbose_name='Sale percent')),
                ('season', models.BooleanField(default=False, verbose_name='Season')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentIntent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='pending', max_length=240, verbose_name='Status')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Amount')),
                ('intent', models.CharField(max_length=240, verbose_name='Intent')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store2Customer', to='store2.customer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('paymentIntent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store2.paymentintent')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store2.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store2UserOrderItem', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('paymentIntent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store2.paymentintent')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store2.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store2UserCartItem', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
