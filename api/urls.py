"""
URL configuration for API app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExampleTableViewSet, CustomerViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'examples', ExampleTableViewSet, basename='example')
router.register(r'customers', CustomerViewSet, basename='customer')

# The API URLs are determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
