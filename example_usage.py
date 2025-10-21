"""
Example usage script demonstrating how to interact with the Sybase API.

This script shows various ways to query the API with pagination, filtering, and ordering.
"""
import requests
from typing import Dict, Any, Optional, List


class SybaseAPIClient:
    """Client for interacting with the Sybase Database API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the API client."""
        self.base_url = base_url
    
    def health_check(self) -> Dict[str, Any]:
        """Check API and database health."""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def execute_query(
        self,
        sql_query: str,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Execute a custom SQL query with pagination, filtering, and ordering.
        
        Args:
            sql_query: SQL SELECT query to execute
            page: Page number (1-indexed)
            page_size: Number of records per page
            filters: Dictionary of column filters
            order_by: List of order clauses (e.g., ["id DESC", "name ASC"])
        
        Returns:
            API response with data and pagination info
        """
        url = f"{self.base_url}/query"
        params = {"page": page, "page_size": page_size}
        
        body = {
            "sql_query": sql_query,
            "filters": filters,
            "order_by": order_by
        }
        
        response = requests.post(url, params=params, json=body)
        response.raise_for_status()
        return response.json()


def example_basic_query():
    """Example: Basic query with pagination."""
    print("\n=== Example 1: Basic Query ===")
    
    client = SybaseAPIClient()
    
    # Execute a simple query
    result = client.execute_query(
        sql_query="SELECT * FROM your_table",
        page=1,
        page_size=10
    )
    
    print(f"Total records: {result['pagination']['total_records']}")
    print(f"Total pages: {result['pagination']['total_pages']}")
    print(f"Current page: {result['pagination']['page']}")
    print(f"Records returned: {len(result['data'])}")


def example_with_filters():
    """Example: Query with filters."""
    print("\n=== Example 2: Query with Filters ===")
    
    client = SybaseAPIClient()
    
    # Execute query with filters
    result = client.execute_query(
        sql_query="SELECT id, name, status FROM users",
        filters={
            "status": "active",
            "role": "admin"
        },
        page=1,
        page_size=20
    )
    
    print(f"Filters applied: {result['filters']}")
    print(f"Records found: {result['pagination']['total_records']}")
    print(f"First few records:")
    for record in result['data'][:3]:
        print(f"  - {record}")


def example_with_ordering():
    """Example: Query with ordering."""
    print("\n=== Example 3: Query with Ordering ===")
    
    client = SybaseAPIClient()
    
    # Execute query with ordering
    result = client.execute_query(
        sql_query="SELECT id, name, created_at FROM products",
        order_by=["created_at DESC", "name ASC"],
        page=1,
        page_size=15
    )
    
    print(f"Order by: {result['order_by']}")
    print(f"Records returned: {len(result['data'])}")


def example_pagination():
    """Example: Iterating through pages."""
    print("\n=== Example 4: Pagination ===")
    
    client = SybaseAPIClient()
    
    # Get first page
    page = 1
    page_size = 10
    
    while True:
        result = client.execute_query(
            sql_query="SELECT * FROM items",
            page=page,
            page_size=page_size
        )
        
        pagination = result['pagination']
        print(f"Page {pagination['page']}/{pagination['total_pages']}")
        print(f"  Records on this page: {len(result['data'])}")
        
        if not pagination['has_next']:
            print("  Last page reached!")
            break
        
        page += 1
        
        # Limit iteration for demo
        if page > 3:
            print("  (Stopping after 3 pages for demo)")
            break


def example_combined():
    """Example: Query with all features combined."""
    print("\n=== Example 5: Combined Features ===")
    
    client = SybaseAPIClient()
    
    # Execute query with filters, ordering, and pagination
    result = client.execute_query(
        sql_query="SELECT id, name, category, price FROM products",
        filters={
            "category": "electronics"
        },
        order_by=["price DESC"],
        page=1,
        page_size=5
    )
    
    print(f"Query: Electronics products ordered by price (descending)")
    print(f"Total matching records: {result['pagination']['total_records']}")
    print(f"\nTop 5 products:")
    for idx, product in enumerate(result['data'], 1):
        print(f"  {idx}. {product}")


def main():
    """Run all examples."""
    print("=" * 60)
    print("Sybase Database API - Usage Examples")
    print("=" * 60)
    
    # Initialize client
    client = SybaseAPIClient()
    
    # Check health
    try:
        health = client.health_check()
        print(f"\nAPI Status: {health['status']}")
        print(f"Database: {health['database']}")
        print(f"Message: {health['message']}")
    except Exception as e:
        print(f"\nError connecting to API: {e}")
        print("Make sure the API server is running on http://localhost:8000")
        return
    
    # Run examples (these will fail without a real database)
    print("\n" + "=" * 60)
    print("Note: The following examples require a configured database")
    print("=" * 60)
    
    try:
        # Uncomment to run examples when database is configured
        # example_basic_query()
        # example_with_filters()
        # example_with_ordering()
        # example_pagination()
        # example_combined()
        
        print("\nTo run query examples, uncomment the function calls in main()")
        print("and configure your database connection in .env file")
    except Exception as e:
        print(f"\nExample execution error: {e}")


if __name__ == "__main__":
    main()
