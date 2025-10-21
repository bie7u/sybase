"""
Admin configuration for API app.
"""
from django.contrib import admin
from .models import ExampleTable, Customer


@admin.register(ExampleTable)
class ExampleTableAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'first_name', 'last_name', 'email', 'city', 'country', 'created_date']
    list_filter = ['country', 'city', 'created_date']
    search_fields = ['first_name', 'last_name', 'email', 'city', 'country']
    ordering = ['last_name', 'first_name']
