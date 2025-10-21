"""
Models for API app.

These models map to existing Sybase database tables.
Set 'managed = False' in Meta to prevent Django from creating/altering tables.
"""
from django.db import models


class ExampleTable(models.Model):
    """
    Example model that maps to an existing Sybase table.
    
    Replace this with your actual table structure.
    To generate models from existing database, use:
    python manage.py inspectdb > models.py
    """
    id = models.AutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(blank=True, null=True, db_column='description')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')
    is_active = models.BooleanField(default=True, db_column='is_active')
    
    class Meta:
        # Set to False because tables already exist in Sybase database
        managed = False
        db_table = 'example_table'
        ordering = ['-created_at']
        verbose_name = 'Example Table'
        verbose_name_plural = 'Example Tables'
    
    def __str__(self):
        return self.name


class Customer(models.Model):
    """
    Example Customer model mapping to existing Sybase table.
    """
    customer_id = models.AutoField(primary_key=True, db_column='customer_id')
    first_name = models.CharField(max_length=100, db_column='first_name')
    last_name = models.CharField(max_length=100, db_column='last_name')
    email = models.EmailField(unique=True, db_column='email')
    phone = models.CharField(max_length=20, blank=True, null=True, db_column='phone')
    address = models.TextField(blank=True, null=True, db_column='address')
    city = models.CharField(max_length=100, blank=True, null=True, db_column='city')
    country = models.CharField(max_length=100, blank=True, null=True, db_column='country')
    created_date = models.DateTimeField(auto_now_add=True, db_column='created_date')
    
    class Meta:
        managed = False
        db_table = 'customers'
        ordering = ['last_name', 'first_name']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
