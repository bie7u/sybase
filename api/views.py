"""
Views for API app.

These views use Django REST Framework to provide API endpoints
with pagination and filtering support.
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import ExampleTable, Customer
from .serializers import (
    ExampleTableSerializer,
    CustomerSerializer,
    CustomerListSerializer
)
from .filters import ExampleTableFilter, CustomerFilter


class ExampleTableViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ExampleTable model.
    
    Provides CRUD operations with pagination and filtering.
    
    Endpoints:
    - GET /api/examples/ - List all examples (paginated)
    - POST /api/examples/ - Create new example
    - GET /api/examples/{id}/ - Retrieve specific example
    - PUT /api/examples/{id}/ - Update example
    - PATCH /api/examples/{id}/ - Partial update example
    - DELETE /api/examples/{id}/ - Delete example
    
    Filters:
    - name: Filter by name (case-insensitive contains)
    - description: Filter by description (case-insensitive contains)
    - is_active: Filter by active status
    - created_after: Filter by creation date (greater than or equal)
    - created_before: Filter by creation date (less than or equal)
    
    Search:
    - search: Search in name and description fields
    
    Ordering:
    - ordering: Order by any field (use - for descending, e.g., -created_at)
    """
    queryset = ExampleTable.objects.all()
    serializer_class = ExampleTableSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ExampleTableFilter
    search_fields = ['name', 'description']
    ordering_fields = ['id', 'name', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active examples."""
        queryset = self.filter_queryset(self.get_queryset().filter(is_active=True))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Customer model.
    
    Provides CRUD operations with pagination and filtering.
    
    Endpoints:
    - GET /api/customers/ - List all customers (paginated)
    - POST /api/customers/ - Create new customer
    - GET /api/customers/{id}/ - Retrieve specific customer
    - PUT /api/customers/{id}/ - Update customer
    - PATCH /api/customers/{id}/ - Partial update customer
    - DELETE /api/customers/{id}/ - Delete customer
    - GET /api/customers/by_country/ - Group customers by country
    
    Filters:
    - first_name: Filter by first name (case-insensitive contains)
    - last_name: Filter by last name (case-insensitive contains)
    - email: Filter by email (case-insensitive contains)
    - city: Filter by city (case-insensitive contains)
    - country: Filter by country (case-insensitive contains)
    - created_after: Filter by creation date (greater than or equal)
    - created_before: Filter by creation date (less than or equal)
    
    Search:
    - search: Search in first_name, last_name, email, city, and country
    
    Ordering:
    - ordering: Order by any field (use - for descending, e.g., -last_name)
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CustomerFilter
    search_fields = ['first_name', 'last_name', 'email', 'city', 'country']
    ordering_fields = ['customer_id', 'first_name', 'last_name', 'email', 'city', 'country', 'created_date']
    ordering = ['last_name', 'first_name']
    
    def get_serializer_class(self):
        """Use different serializers for list and detail views."""
        if self.action == 'list':
            return CustomerListSerializer
        return CustomerSerializer
    
    @action(detail=False, methods=['get'])
    def by_country(self, request):
        """Get customers grouped by country."""
        from django.db.models import Count
        countries = Customer.objects.values('country').annotate(
            count=Count('customer_id')
        ).order_by('-count')
        return Response(countries)
