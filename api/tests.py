"""
Tests for API app.

Note: These are example tests. In production, you would need a test database
and actual test data to run these tests properly.
"""
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse


class ExampleTableAPITestCase(APITestCase):
    """
    Test cases for ExampleTable API endpoints.
    
    Note: Since models have managed=False, these tests won't create tables.
    You need to ensure test tables exist in your test database.
    """
    
    def setUp(self):
        """Set up test client."""
        self.client = APIClient()
        self.list_url = reverse('example-list')
    
    def test_list_examples(self):
        """Test listing examples endpoint."""
        response = self.client.get(self.list_url)
        # In real tests, check for status 200
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_examples_with_pagination(self):
        """Test listing examples with pagination."""
        response = self.client.get(self.list_url, {'page': 1, 'page_size': 5})
        # Verify pagination parameters
    
    def test_list_examples_with_filter(self):
        """Test listing examples with filter."""
        response = self.client.get(self.list_url, {'is_active': True})
        # Verify filtering works
    
    def test_list_examples_with_search(self):
        """Test listing examples with search."""
        response = self.client.get(self.list_url, {'search': 'test'})
        # Verify search works
    
    def test_list_examples_with_ordering(self):
        """Test listing examples with ordering."""
        response = self.client.get(self.list_url, {'ordering': '-created_at'})
        # Verify ordering works


class CustomerAPITestCase(APITestCase):
    """
    Test cases for Customer API endpoints.
    """
    
    def setUp(self):
        """Set up test client."""
        self.client = APIClient()
        self.list_url = reverse('customer-list')
    
    def test_list_customers(self):
        """Test listing customers endpoint."""
        response = self.client.get(self.list_url)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_customers_with_city_filter(self):
        """Test filtering customers by city."""
        response = self.client.get(self.list_url, {'city': 'Warsaw'})
        # Verify city filter works
    
    def test_list_customers_with_country_filter(self):
        """Test filtering customers by country."""
        response = self.client.get(self.list_url, {'country': 'Poland'})
        # Verify country filter works
    
    def test_list_customers_with_search(self):
        """Test searching customers."""
        response = self.client.get(self.list_url, {'search': 'john'})
        # Verify search works across multiple fields
    
    def test_list_customers_with_ordering(self):
        """Test ordering customers."""
        response = self.client.get(self.list_url, {'ordering': 'last_name'})
        # Verify ordering works
    
    def test_customers_by_country(self):
        """Test custom by_country endpoint."""
        url = reverse('customer-by-country')
        response = self.client.get(url)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify response contains country groupings


class DatabaseConnectionTestCase(TestCase):
    """
    Test database connection and basic operations.
    """
    
    def test_database_connection(self):
        """Test that database connection works."""
        from django.db import connection
        with connection.cursor() as cursor:
            # This should not raise an exception if connection works
            # cursor.execute("SELECT 1")
            pass
    
    def test_can_query_models(self):
        """Test that we can query models."""
        # from api.models import Customer
        # Try to query (might fail if tables don't exist in test DB)
        # customers = Customer.objects.all()
        pass


class FilterTestCase(TestCase):
    """
    Test cases for filters.
    """
    
    def test_example_table_filter(self):
        """Test ExampleTableFilter."""
        from api.filters import ExampleTableFilter
        # Test filter initialization
        filter_instance = ExampleTableFilter()
        self.assertIsNotNone(filter_instance)
    
    def test_customer_filter(self):
        """Test CustomerFilter."""
        from api.filters import CustomerFilter
        # Test filter initialization
        filter_instance = CustomerFilter()
        self.assertIsNotNone(filter_instance)


class SerializerTestCase(TestCase):
    """
    Test cases for serializers.
    """
    
    def test_example_table_serializer(self):
        """Test ExampleTableSerializer."""
        from api.serializers import ExampleTableSerializer
        # Test serializer can be instantiated
        serializer = ExampleTableSerializer()
        self.assertIsNotNone(serializer)
    
    def test_customer_serializer(self):
        """Test CustomerSerializer."""
        from api.serializers import CustomerSerializer
        # Test serializer can be instantiated
        serializer = CustomerSerializer()
        self.assertIsNotNone(serializer)
        # Verify full_name method exists
        self.assertTrue(hasattr(serializer, 'get_full_name'))
