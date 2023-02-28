import django_filters
from django.db.models import Q
from django_filters import OrderingFilter

from .models import Product


class ProductFilter(django_filters.FilterSet):
    s = django_filters.CharFilter(method='my_custom_search', label="Search")

    o = OrderingFilter(
        fields=(
            ('price', 'price')
        ),
        field_labels={
            'price': 'по возрастанию',
            '-price': 'по убыванию',
        }
    )

    class Meta:
        model = Product
        fields = ['category', 'brand', 'animal']

    def my_custom_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value) |
            Q(category__name__icontains=value) |
            Q(brand__name__icontains=value) |
            Q(animal__name__icontains=value)
        )
