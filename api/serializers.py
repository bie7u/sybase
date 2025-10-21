"""
Serializers for API app.

These serializers convert model instances to JSON and vice versa.
"""
from rest_framework import serializers
from .models import ExampleTable, Customer


class ExampleTableSerializer(serializers.ModelSerializer):
    """
    Serializer for ExampleTable model.
    """
    class Meta:
        model = ExampleTable
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for Customer model.
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Customer
        fields = [
            'customer_id', 'first_name', 'last_name', 'full_name',
            'email', 'phone', 'address', 'city', 'country', 'created_date'
        ]
        read_only_fields = ['customer_id', 'created_date']
    
    def get_full_name(self, obj):
        """Return full name of the customer."""
        return f"{obj.first_name} {obj.last_name}"


class CustomerListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing customers.
    """
    class Meta:
        model = Customer
        fields = ['customer_id', 'first_name', 'last_name', 'email', 'city', 'country']
