# Project Structure

```
sybase/
├── 📄 README.md                    # Main documentation
├── 📄 QUICKSTART.md                # 5-minute getting started guide
├── 📄 SECURITY.md                  # Security guidelines and best practices
├── 📄 SECURITY_SUMMARY.md          # CodeQL analysis and security summary
├── 📄 API_EXAMPLES.md              # Comprehensive API usage examples
│
├── 🐍 Core Application Files
│   ├── main.py                     # FastAPI application and endpoints
│   ├── config.py                   # Configuration management
│   ├── database.py                 # Database connection setup
│   ├── query_builder.py            # Query building with security validation
│   └── models.py                   # Pydantic models for validation
│
├── 📦 Dependencies
│   ├── requirements.txt            # Production dependencies
│   └── requirements-dev.txt        # Development/testing dependencies
│
├── 🧪 Examples & Tests
│   ├── example_usage.py            # Python client example
│   └── test_example.py             # Example test cases
│
├── 🐳 Docker
│   ├── Dockerfile                  # Container definition
│   ├── docker-compose.yml          # Compose configuration
│   └── .dockerignore               # Docker ignore patterns
│
└── ⚙️ Configuration
    ├── .env.example                # Environment variables template
    └── .gitignore                  # Git ignore patterns
```

## File Descriptions

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Complete API documentation, installation, and usage guide |
| `QUICKSTART.md` | Quick start guide to get running in 5 minutes |
| `SECURITY.md` | Security considerations and production recommendations |
| `SECURITY_SUMMARY.md` | CodeQL analysis results and security assessment |
| `API_EXAMPLES.md` | Comprehensive examples for all API operations |

### Core Application Files

| File | Purpose |
|------|---------|
| `main.py` | FastAPI application with endpoint definitions |
| `config.py` | Configuration management using Pydantic settings |
| `database.py` | SQLAlchemy engine and session management |
| `query_builder.py` | Query construction with pagination, filtering, ordering |
| `models.py` | Pydantic models for request/response validation |

### Dependencies

| File | Purpose |
|------|---------|
| `requirements.txt` | Production dependencies (FastAPI, SQLAlchemy, etc.) |
| `requirements-dev.txt` | Development dependencies (pytest, httpx, etc.) |

### Examples & Tests

| File | Purpose |
|------|---------|
| `example_usage.py` | Python client demonstrating API usage |
| `test_example.py` | Example test cases for the API |

### Docker Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Container image definition |
| `docker-compose.yml` | Multi-container orchestration |
| `.dockerignore` | Files to exclude from Docker build |

### Configuration Files

| File | Purpose |
|------|---------|
| `.env.example` | Template for environment variables |
| `.gitignore` | Git ignore patterns |

## Key Features by Module

### main.py
- FastAPI application setup
- Health check endpoint
- Custom query endpoint with validation
- Example endpoints (users, products)
- Error handling

### query_builder.py
- QueryBuilder class for SQL construction
- Identifier validation (SQL injection prevention)
- Parameterized query support
- Pagination with OFFSET-FETCH
- Dynamic filtering
- Multi-column ordering
- Count query generation

### database.py
- SQLAlchemy engine configuration
- Connection pooling
- Session management
- Database health check

### models.py
- QueryParams (pagination + filters + ordering)
- PaginationInfo (metadata)
- QueryResponse (standardized response)
- HealthCheckResponse

### config.py
- Environment-based configuration
- Database URL construction
- API server settings

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/query` | Execute custom SQL query |
| GET | `/api/v1/example/users` | Example: Get users |
| GET | `/api/v1/example/products` | Example: Get products |
| GET | `/docs` | Swagger UI documentation |
| GET | `/redoc` | ReDoc documentation |

## Data Flow

```
Client Request
    ↓
FastAPI Endpoint (main.py)
    ↓
Input Validation (models.py)
    ↓
Database Session (database.py)
    ↓
Query Building (query_builder.py)
    ├─ Identifier Validation
    ├─ Filter Application
    ├─ Ordering Application
    └─ Pagination Application
    ↓
SQLAlchemy Execution
    ↓
Response Formatting
    ↓
JSON Response to Client
```

## Security Layers

1. **Input Validation** (Pydantic models)
2. **Query Type Validation** (SELECT only)
3. **Identifier Validation** (Column/table names)
4. **Parameterized Queries** (Filter values)
5. **Connection Pooling** (Resource management)

## Environment Variables

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5000
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
DB_DRIVER=pymssql

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

## Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python main.py

# Run with Docker
docker-compose up -d

# Run tests
pytest test_example.py

# View logs
docker-compose logs -f
```
