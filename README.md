# Sybase Database API

A FastAPI-based REST API for querying Sybase databases with built-in support for pagination, filtering, and ordering. This API allows you to execute raw SQL queries while providing a clean interface for common data operations.

## Features

- 🚀 **FastAPI Framework**: High-performance, modern Python web framework
- 🔌 **SQLAlchemy Integration**: Robust database connectivity with connection pooling
- 📄 **Pagination Support**: Efficient pagination using OFFSET-FETCH
- 🔍 **Dynamic Filtering**: Filter results by any column with key-value pairs
- 📊 **Flexible Ordering**: Sort results by multiple columns (ASC/DESC)
- 🔒 **Raw SQL Support**: Execute custom SQL queries with safety checks
- 📝 **Auto-generated API Documentation**: Interactive Swagger UI and ReDoc

## Quick Start

See [QUICKSTART.md](QUICKSTART.md) for a 5-minute getting started guide.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/bie7u/sybase.git
cd sybase
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure database connection:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Update `.env` with your Sybase database credentials:
```env
DB_HOST=your_sybase_host
DB_PORT=5000
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_DRIVER=pymssql
```

## Usage

### Starting the API Server

**Option 1: Direct Python execution**
```bash
python main.py
```

**Option 2: Using Uvicorn**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Option 3: Using Docker**
```bash
# Build and run with docker-compose
docker-compose up -d

# Or build and run with Docker directly
docker build -t sybase-api .
docker run -p 8000:8000 --env-file .env sybase-api
```

The API will be available at:
- API: http://localhost:8000
- Interactive Documentation (Swagger UI): http://localhost:8000/docs
- Alternative Documentation (ReDoc): http://localhost:8000/redoc

### API Endpoints

#### 1. Health Check
```bash
GET /health
```

Check API and database connectivity status.

#### 2. Custom Query Endpoint
```bash
POST /query
```

Execute a custom SQL query with pagination, filtering, and ordering.

**Request Body:**
```json
{
  "sql_query": "SELECT id, name, email FROM users",
  "filters": {
    "status": "active",
    "role": "admin"
  },
  "order_by": ["id DESC", "name ASC"]
}
```

**Query Parameters:**
- `page` (optional): Page number, default: 1
- `page_size` (optional): Records per page, default: 10 (max: 100)

**Example with curl:**
```bash
curl -X POST "http://localhost:8000/query?page=1&page_size=10" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT * FROM your_table",
    "filters": {"column_name": "value"},
    "order_by": ["id DESC"]
  }'
```

#### 3. Example Endpoints

The API includes example endpoints demonstrating common use cases:

**Get Users:**
```bash
GET /api/v1/example/users?page=1&page_size=10&status=active&order_by=id%20DESC
```

**Get Products:**
```bash
GET /api/v1/example/products?page=1&page_size=10&category=electronics
```

### Response Format

All query endpoints return a standardized response:

```json
{
  "data": [
    {
      "id": 1,
      "name": "Example",
      "email": "user@example.com"
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
  "order_by": ["id DESC"]
}
```

## Creating Custom Endpoints

You can easily create custom endpoints for your specific tables. Here's an example:

```python
@app.get("/api/v1/my-table", response_model=QueryResponse)
async def get_my_table_data(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    filter_column: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    base_query = "SELECT * FROM my_table"
    
    filters = {}
    if filter_column:
        filters["column_name"] = filter_column
    
    result = execute_query_with_pagination(
        db=db,
        base_query=base_query,
        filters=filters,
        order_by=["id DESC"],
        page=page,
        page_size=page_size
    )
    
    return QueryResponse(**result)
```

## Architecture

The application follows a modular architecture:

### Core Modules

- **`main.py`**: FastAPI application with endpoint definitions
- **`database.py`**: Database connection and session management with SQLAlchemy
- **`query_builder.py`**: Query building utilities with security validations
- **`models.py`**: Pydantic models for request/response validation
- **`config.py`**: Configuration management using environment variables

### Additional Files

- **`example_usage.py`**: Example Python client demonstrating API usage
- **`test_example.py`**: Example test cases for the API
- **`requirements.txt`**: Production dependencies
- **`requirements-dev.txt`**: Development and testing dependencies
- **`Dockerfile`**: Docker container configuration
- **`docker-compose.yml`**: Docker Compose orchestration

### Documentation

- **`README.md`**: Main documentation (this file)
- **`QUICKSTART.md`**: Quick start guide
- **`SECURITY.md`**: Security guidelines and best practices

## Query Builder

The `QueryBuilder` class provides a flexible way to construct SQL queries:

```python
from query_builder import QueryBuilder

builder = QueryBuilder("SELECT * FROM users")

# Build query with filters, ordering, and pagination
query, params = builder.build(
    filters={"status": "active"},
    order_by=["created_at DESC"],
    page=1,
    page_size=20
)

# Get count query for pagination
count_query, count_params = builder.get_count_query(
    filters={"status": "active"}
)
```

## Security Considerations

This API implements several security measures:

1. **SQL Injection Prevention**: 
   - Parameterized queries for all filter values
   - Strict identifier validation for column names
   - Query structure validation
2. **Query Validation**: Only SELECT queries are allowed in the custom query endpoint
3. **Input Validation**: Pydantic models validate all input parameters
4. **Connection Pooling**: SQLAlchemy manages database connections securely

**Important:** The `/query` endpoint accepts user-provided SQL queries. For production use, it's recommended to:
- Place this endpoint behind authentication/authorization
- Consider disabling it and using dedicated endpoints instead
- Review [SECURITY.md](SECURITY.md) for detailed security guidelines

## Configuration

All configuration is managed through environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| DB_HOST | Database host | localhost |
| DB_PORT | Database port | 5000 |
| DB_NAME | Database name | master |
| DB_USER | Database username | sa |
| DB_PASSWORD | Database password | (empty) |
| DB_DRIVER | SQLAlchemy driver | pymssql |
| API_HOST | API server host | 0.0.0.0 |
| API_PORT | API server port | 8000 |

## Development

### Running Tests

The application structure supports easy testing. Example test structure:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
```

### Code Structure

```
sybase/
├── main.py              # FastAPI application
├── database.py          # Database connectivity
├── query_builder.py     # Query construction utilities
├── models.py            # Pydantic models
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
└── README.md           # Documentation
```

## Dependencies

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **pymssql**: Python driver for Microsoft SQL Server/Sybase
- **Uvicorn**: ASGI server for running FastAPI
- **Pydantic**: Data validation using Python type annotations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on GitHub.