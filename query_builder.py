"""
Query builder utilities for handling pagination, filtering, and ordering.
"""
from typing import Dict, List, Optional, Any, Tuple
from sqlalchemy import text
from sqlalchemy.orm import Session
import re


class QueryBuilder:
    """
    A utility class to build SQL queries with pagination, filtering, and ordering.
    """
    
    # Regex pattern for valid SQL identifiers (column/table names)
    IDENTIFIER_PATTERN = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)?$')
    
    def __init__(self, base_query: str):
        """
        Initialize QueryBuilder with a base SQL query.
        
        Args:
            base_query: The base SQL SELECT query (without pagination/filtering/ordering)
        """
        self.base_query = base_query.strip()
        if self.base_query.endswith(';'):
            self.base_query = self.base_query[:-1]
    
    @staticmethod
    def validate_identifier(identifier: str) -> bool:
        """
        Validate that a string is a safe SQL identifier.
        
        Args:
            identifier: The identifier to validate (column or table name)
            
        Returns:
            True if valid, False otherwise
        """
        return bool(QueryBuilder.IDENTIFIER_PATTERN.match(identifier))
    
    @staticmethod
    def sanitize_identifier(identifier: str) -> str:
        """
        Sanitize and validate a SQL identifier.
        
        Args:
            identifier: The identifier to sanitize
            
        Returns:
            The sanitized identifier
            
        Raises:
            ValueError: If the identifier is invalid
        """
        # Remove any whitespace
        identifier = identifier.strip()
        
        if not QueryBuilder.validate_identifier(identifier):
            raise ValueError(f"Invalid SQL identifier: {identifier}")
        
        return identifier
    
    def apply_filters(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Apply filters to the query.
        
        Args:
            query: The SQL query to filter
            filters: Dictionary of column_name: value pairs
            
        Returns:
            Tuple of (modified_query, params_dict)
            
        Raises:
            ValueError: If any column name is invalid
        """
        if not filters:
            return query, {}
        
        params = {}
        where_clauses = []
        
        # Check if WHERE clause already exists
        has_where = 'WHERE' in query.upper()
        
        for idx, (column, value) in enumerate(filters.items()):
            # Validate column name to prevent SQL injection
            sanitized_column = self.sanitize_identifier(column)
            
            param_name = f"filter_{idx}"
            if value is None:
                where_clauses.append(f"{sanitized_column} IS NULL")
            else:
                where_clauses.append(f"{sanitized_column} = :{param_name}")
                params[param_name] = value
        
        if where_clauses:
            connector = "AND" if has_where else "WHERE"
            query = f"{query} {connector} {' AND '.join(where_clauses)}"
        
        return query, params
    
    def apply_ordering(
        self,
        query: str,
        order_by: Optional[List[str]] = None
    ) -> str:
        """
        Apply ordering to the query.
        
        Args:
            query: The SQL query to order
            order_by: List of column names with optional direction (e.g., ["id DESC", "name ASC"])
            
        Returns:
            Modified query with ORDER BY clause
            
        Raises:
            ValueError: If any column name is invalid
        """
        if not order_by:
            return query
        
        # Validate and sanitize order_by clauses
        order_clauses = []
        for order in order_by:
            parts = order.strip().split()
            if len(parts) == 1:
                # Just column name, default to ASC
                sanitized_column = self.sanitize_identifier(parts[0])
                order_clauses.append(f"{sanitized_column} ASC")
            elif len(parts) == 2 and parts[1].upper() in ['ASC', 'DESC']:
                # Column name with direction
                sanitized_column = self.sanitize_identifier(parts[0])
                order_clauses.append(f"{sanitized_column} {parts[1].upper()}")
            else:
                # Invalid format, raise error
                raise ValueError(f"Invalid order_by format: {order}")
        
        if order_clauses:
            query = f"{query} ORDER BY {', '.join(order_clauses)}"
        
        return query
    
    def apply_pagination(
        self,
        query: str,
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[str, Dict[str, int]]:
        """
        Apply pagination to the query using OFFSET and FETCH.
        
        Args:
            query: The SQL query to paginate
            page: Page number (1-indexed)
            page_size: Number of records per page
            
        Returns:
            Tuple of (modified_query, params_dict)
        """
        # Ensure page is at least 1
        page = max(1, page)
        page_size = max(1, page_size)
        
        offset = (page - 1) * page_size
        
        # Use OFFSET-FETCH for SQL Server/Sybase
        # Note: OFFSET-FETCH requires ORDER BY clause
        if 'ORDER BY' not in query.upper():
            # Add a default ORDER BY if none exists
            query = f"{query} ORDER BY (SELECT NULL)"
        
        query = f"{query} OFFSET :offset ROWS FETCH NEXT :page_size ROWS ONLY"
        
        params = {
            'offset': offset,
            'page_size': page_size
        }
        
        return query, params
    
    def build(
        self,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[List[str]] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Build complete query with filters, ordering, and pagination.
        
        Args:
            filters: Dictionary of column_name: value pairs
            order_by: List of column names with optional direction
            page: Page number (1-indexed)
            page_size: Number of records per page
            
        Returns:
            Tuple of (final_query, all_params)
        """
        query = self.base_query
        all_params = {}
        
        # Apply filters
        query, filter_params = self.apply_filters(query, filters)
        all_params.update(filter_params)
        
        # Apply ordering
        query = self.apply_ordering(query, order_by)
        
        # Apply pagination
        query, pagination_params = self.apply_pagination(query, page, page_size)
        all_params.update(pagination_params)
        
        return query, all_params
    
    def get_count_query(
        self,
        filters: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Build a COUNT query for getting total records.
        
        Args:
            filters: Dictionary of column_name: value pairs
            
        Returns:
            Tuple of (count_query, params)
        """
        # Extract the FROM clause and beyond from the base query
        query_upper = self.base_query.upper()
        from_index = query_upper.find('FROM')
        
        if from_index == -1:
            raise ValueError("Base query must contain a FROM clause")
        
        from_clause = self.base_query[from_index:]
        count_query = f"SELECT COUNT(*) as total {from_clause}"
        
        # Apply filters to count query
        count_query, params = self.apply_filters(count_query, filters)
        
        return count_query, params


def execute_query_with_pagination(
    db: Session,
    base_query: str,
    filters: Optional[Dict[str, Any]] = None,
    order_by: Optional[List[str]] = None,
    page: int = 1,
    page_size: int = 10
) -> Dict[str, Any]:
    """
    Execute a query with pagination, filtering, and ordering.
    
    Security Note: The base_query parameter accepts user-provided SQL, which is
    intentional functionality. Callers must validate that base_query is a SELECT
    statement before calling this function. Column names in filters and order_by
    are validated using identifier validation to prevent SQL injection.
    
    Args:
        db: Database session
        base_query: Base SQL SELECT query (must be validated by caller)
        filters: Dictionary of column_name: value pairs (column names are validated)
        order_by: List of column names with optional direction (column names are validated)
        page: Page number (1-indexed)
        page_size: Number of records per page
        
    Returns:
        Dictionary containing data, pagination info, and metadata
    """
    builder = QueryBuilder(base_query)
    
    # Get total count
    count_query, count_params = builder.get_count_query(filters)
    total_result = db.execute(text(count_query), count_params).fetchone()
    total_records = total_result[0] if total_result else 0
    
    # Build and execute main query
    final_query, query_params = builder.build(filters, order_by, page, page_size)
    result = db.execute(text(final_query), query_params)
    
    # Convert results to list of dictionaries
    columns = result.keys()
    data = [dict(zip(columns, row)) for row in result.fetchall()]
    
    # Calculate pagination metadata
    total_pages = (total_records + page_size - 1) // page_size if page_size > 0 else 0
    
    return {
        "data": data,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_records": total_records,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1
        },
        "filters": filters or {},
        "order_by": order_by or []
    }
