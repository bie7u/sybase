"""
Pydantic models for API request/response validation.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class PaginationParams(BaseModel):
    """Parameters for pagination."""
    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(default=10, ge=1, le=100, description="Number of records per page")


class QueryParams(BaseModel):
    """Parameters for query execution with pagination, filtering, and ordering."""
    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(default=10, ge=1, le=100, description="Number of records per page")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Filters as key-value pairs")
    order_by: Optional[List[str]] = Field(default=None, description="List of columns to order by (e.g., ['id DESC', 'name ASC'])")


class PaginationInfo(BaseModel):
    """Pagination information in response."""
    page: int
    page_size: int
    total_records: int
    total_pages: int
    has_next: bool
    has_previous: bool


class QueryResponse(BaseModel):
    """Standard response format for queries."""
    data: List[Dict[str, Any]]
    pagination: PaginationInfo
    filters: Dict[str, Any]
    order_by: List[str]


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str
    database: str
    message: str
