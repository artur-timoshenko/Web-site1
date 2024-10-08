import django_filters
from .models import Product
from django_filters.widgets import RangeWidget
from django.db.models import Max, Min


# class UserFilter(django_filters.FilterSet):
#     class Meta:
#         model = User
#         fields = {
#             'username': ['icontains'],
#             'password': ['icontains'],
#             'email': ['icontains'],
#             'phone': ['icontains'],
#             'photo': ['exact'],
#             # 'price': ['lt', 'gt'],
#         }


class ProductFilter(django_filters.FilterSet):
    # title = django_filters.CharFilter(lookup_expr='icontains')
    # description = django_filters.CharFilter(lookup_expr='icontains')

    price__max = Product.objects.aggregate(Max('price')).get('price__max', 0)
    price__min = Product.objects.aggregate(Min('price')).get('price__min', 0)

    rangeWidget = RangeWidget(attrs={'type': 'range', 'min': price__min, 'max': price__max})
    rangeWidget.widgets[0].attrs.update({'value': price__min})
    rangeWidget.widgets[1].attrs.update({'value': price__max})

    price = django_filters.RangeFilter(widget=rangeWidget)

    class Meta:
        model = Product
        fields = {
            'title': ['icontains'],
            'description': ['icontains'],
            'price': ['lte', 'gte'],
        }
