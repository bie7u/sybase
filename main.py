"""
FastAPI application for Sybase database API with pagination, filtering, and ordering.
"""
from fastapi import FastAPI, Depends, HTTPException, Query, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional

from database import get_db, test_connection
from query_builder import execute_query_with_pagination
from models import QueryResponse, HealthCheckResponse, QueryParams
from config import settings

# Create FastAPI application
app = FastAPI(
    title="Sybase Database API",
    description="API for querying Sybase database with pagination, filtering, and ordering support",
    version="1.0.0"
)


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Sybase Database API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "query": "/query (POST)",
            "examples": "/api/v1/..."
        }
    }


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint to verify API and database connectivity.
    """
    db_status = test_connection()
    
    if db_status:
        return HealthCheckResponse(
            status="healthy",
            database="connected",
            message="API and database are operational"
        )
    else:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "message": "Database connection failed"
            }
        )


@app.post("/query", response_model=QueryResponse)
async def execute_custom_query(
    sql_query: str = Body(..., description="SQL SELECT query to execute"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of records per page"),
    filters: Optional[Dict[str, Any]] = Body(None, description="Filters as key-value pairs"),
    order_by: Optional[List[str]] = Body(None, description="List of columns to order by"),
    db: Session = Depends(get_db)
):
    """
    Execute a custom SQL query with pagination, filtering, and ordering.
    
    Example request body:
    ```json
    {
        "sql_query": "SELECT id, name, email FROM users",
        "filters": {"status": "active", "role": "admin"},
        "order_by": ["id DESC", "name ASC"]
    }
    ```
    """
    try:
        # Validate that it's a SELECT query
        if not sql_query.strip().upper().startswith('SELECT'):
            raise HTTPException(
                status_code=400,
                detail="Only SELECT queries are allowed"
            )
        
        result = execute_query_with_pagination(
            db=db,
            base_query=sql_query,
            filters=filters,
            order_by=order_by,
            page=page,
            page_size=page_size
        )
        
        return QueryResponse(**result)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Query execution failed: {str(e)}"
        )


# Example API endpoints for common use cases
@app.get("/api/v1/example/users", response_model=QueryResponse)
async def get_users(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Records per page"),
    status: Optional[str] = Query(None, description="Filter by status"),
    role: Optional[str] = Query(None, description="Filter by role"),
    order_by: Optional[str] = Query("id DESC", description="Order by column(s)"),
    db: Session = Depends(get_db)
):
    """
    Example endpoint: Get users with pagination, filtering, and ordering.
    
    This is a demonstration endpoint. Replace the SQL query with your actual table structure.
    """
    # Base SQL query
    base_query = "SELECT id, name, email, status, role FROM users"
    
    # Build filters dictionary
    filters = {}
    if status:
        filters["status"] = status
    if role:
        filters["role"] = role
    
    # Parse order_by parameter
    order_by_list = [order_by] if order_by else None
    
    try:
        result = execute_query_with_pagination(
            db=db,
            base_query=base_query,
            filters=filters if filters else None,
            order_by=order_by_list,
            page=page,
            page_size=page_size
        )
        
        return QueryResponse(**result)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Query execution failed: {str(e)}"
        )


@app.get("/api/v1/example/products", response_model=QueryResponse)
async def get_products(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Records per page"),
    category: Optional[str] = Query(None, description="Filter by category"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    order_by: Optional[str] = Query("id DESC", description="Order by column(s)"),
    db: Session = Depends(get_db)
):
    """
    Example endpoint: Get products with pagination, filtering, and ordering.
    
    This is a demonstration endpoint. Replace the SQL query with your actual table structure.
    """
    # Base SQL query
    base_query = "SELECT id, name, category, price, stock FROM products"
    
    # Build filters dictionary
    filters = {}
    if category:
        filters["category"] = category
    
    # Parse order_by parameter
    order_by_list = [order_by] if order_by else None
    
    try:
        result = execute_query_with_pagination(
            db=db,
            base_query=base_query,
            filters=filters if filters else None,
            order_by=order_by_list,
            page=page,
            page_size=page_size
        )
        
        # Note: min_price filtering would need to be handled differently
        # as it's a range filter, not an equality filter
        # You can extend the query_builder to support operators
        
        return QueryResponse(**result)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Query execution failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
