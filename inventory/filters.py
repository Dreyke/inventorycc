import django_filters
from .models import Product, Brand

class ProductFilter(django_filters.FilterSet):

    CHOICES = (
        ('ascending', 'Ascending'),
        ('descending', 'Descending')
    )

    ordering = django_filters.ChoiceFilter(label='Sort By Date', choices=CHOICES, method='filter_by_order')

    code = django_filters.CharFilter(lookup_expr='exact')
    name = django_filters.CharFilter(lookup_expr='exact')
    brand = django_filters.CharFilter(lookup_expr='exact')
    category = django_filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['code', 'name', 'brand', 'category']

    def filter_by_order(self, queryset, name, value):
        expression = 'date_added' if value == 'ascending' else '-date_added'
        return queryset.order_by(expression)


class BrandFilter(django_filters.FilterSet):

    brand_name = django_filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = Brand
        fields = ['brand_name']