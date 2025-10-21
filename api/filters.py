"""
Filters for API app.

These filters allow users to filter querysets based on various criteria.
"""
import django_filters
from .models import ExampleTable, Customer


class ExampleTableFilter(django_filters.FilterSet):
    """
    Filter for ExampleTable model.
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    is_active = django_filters.BooleanFilter()
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = ExampleTable
        fields = ['name', 'description', 'is_active', 'created_at']


class CustomerFilter(django_filters.FilterSet):
    """
    Filter for Customer model.
    """
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    city = django_filters.CharFilter(lookup_expr='icontains')
    country = django_filters.CharFilter(lookup_expr='icontains')
    created_after = django_filters.DateTimeFilter(field_name='created_date', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_date', lookup_expr='lte')
    
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'city', 'country', 'created_date']
