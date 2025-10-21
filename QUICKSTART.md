# Quick Start Guide

Get up and running with the Sybase Database API in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- Access to a Sybase/Microsoft SQL Server database
- Basic knowledge of SQL and REST APIs

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/bie7u/sybase.git
cd sybase
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Database Connection

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your database credentials:

```env
DB_HOST=your_database_host
DB_PORT=5000
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
```

### 4. Start the Server

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## Your First API Call

### Using curl

```bash
curl -X POST "http://localhost:8000/query?page=1&page_size=10" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT * FROM your_table"
  }'
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    params={"page": 1, "page_size": 10},
    json={"sql_query": "SELECT * FROM your_table"}
)

print(response.json())
```

### Using the Interactive Documentation

1. Open http://localhost:8000/docs in your browser
2. Find the `/query` endpoint
3. Click "Try it out"
4. Enter your SQL query
5. Click "Execute"

## Example Use Cases

### 1. Basic Query with Pagination

```bash
curl -X POST "http://localhost:8000/query?page=1&page_size=20" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT id, name, email FROM users"
  }'
```

### 2. Query with Filters

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT id, name, status FROM users",
    "filters": {
      "status": "active"
    }
  }'
```

### 3. Query with Ordering

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT id, name, created_at FROM users",
    "order_by": ["created_at DESC", "name ASC"]
  }'
```

### 4. Complete Example

```bash
curl -X POST "http://localhost:8000/query?page=2&page_size=15" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT id, name, email, status, created_at FROM users",
    "filters": {
      "status": "active"
    },
    "order_by": ["created_at DESC"]
  }'
```

## Understanding the Response

All queries return a standardized JSON response:

```json
{
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 10,
    "total_records": 100,
    "total_pages": 10,
    "has_next": true,
    "has_previous": false
  },
  "filters": {
    "status": "active"
  },
  "order_by": ["created_at DESC"]
}
```

## Creating Custom Endpoints

For production use, create dedicated endpoints instead of using the generic `/query` endpoint:

```python
# Add to main.py

@app.get("/api/v1/customers")
async def get_customers(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    country: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    base_query = "SELECT id, name, email, country FROM customers"
    
    filters = {}
    if country:
        filters["country"] = country
    
    result = execute_query_with_pagination(
        db=db,
        base_query=base_query,
        filters=filters,
        order_by=["name ASC"],
        page=page,
        page_size=page_size
    )
    
    return QueryResponse(**result)
```

## Testing the API

### Health Check

```bash
curl http://localhost:8000/health
```

### Check API Documentation

Visit http://localhost:8000/docs for interactive Swagger documentation.

## Next Steps

1. **Read the Full Documentation:** Check out [README.md](README.md) for detailed information
2. **Security:** Review [SECURITY.md](SECURITY.md) for security best practices
3. **Customize:** Add authentication, create dedicated endpoints for your tables
4. **Deploy:** Deploy to your preferred hosting platform

## Troubleshooting

### Database Connection Failed

Check your `.env` file and ensure:
- Database host and port are correct
- Database name exists
- Username and password are correct
- Database server is running and accessible

### Module Not Found

Install all dependencies:
```bash
pip install -r requirements.txt
```

### Port Already in Use

Change the port in `.env`:
```env
API_PORT=8080
```

Or specify when running:
```bash
uvicorn main:app --port 8080
```

## Getting Help

- Check the [README.md](README.md) for detailed documentation
- Open an issue on GitHub
- Review the example endpoints in `main.py`
