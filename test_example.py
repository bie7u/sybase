"""
Example test file demonstrating how to test the API endpoints.

Note: These tests require a test database connection to run successfully.
To run tests: pytest test_example.py
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns API information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["message"] == "Sybase Database API"


def test_health_check_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    # Note: This will fail if database is not connected
    # In a real test, you'd mock the database connection
    assert response.status_code in [200, 503]
    data = response.json()
    assert "status" in data
    assert "database" in data


def test_query_endpoint_validation():
    """Test that query endpoint validates SQL queries."""
    # Test with non-SELECT query (should be rejected)
    response = client.post(
        "/query",
        json={
            "sql_query": "DELETE FROM users"
        }
    )
    assert response.status_code == 400
    assert "Only SELECT queries are allowed" in response.json()["detail"]


def test_query_endpoint_with_select():
    """Test query endpoint with a SELECT query."""
    # This test would require a mock database or test database
    # Here's how you'd structure it with a mock:
    
    with patch('main.get_db') as mock_get_db:
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # You would set up mock returns here
        # This is just a structure example
        pass


def test_pagination_params():
    """Test pagination parameter validation."""
    # Test with valid pagination
    response = client.post(
        "/query?page=1&page_size=10",
        json={
            "sql_query": "SELECT 1"
        }
    )
    # Would need database connection to succeed
    assert response.status_code in [200, 500]
    
    # Test with invalid page (should be converted to valid)
    response = client.post(
        "/query?page=0&page_size=10",
        json={
            "sql_query": "SELECT 1"
        }
    )
    # Page 0 should be rejected by Query validation
    assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
