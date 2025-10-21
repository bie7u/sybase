# Security Considerations

## Overview

This API is designed to provide flexible access to Sybase databases while implementing security measures to prevent SQL injection and other vulnerabilities.

## Security Features

### 1. SQL Injection Prevention

#### Identifier Validation
All column names used in filters and ordering are validated using a strict pattern that only allows:
- Alphanumeric characters (a-z, A-Z, 0-9)
- Underscores (_)
- Dots (.) for table-qualified names (e.g., `table.column`)
- Must start with a letter or underscore

Invalid identifiers are rejected with a `ValueError`.

**Examples:**
```python
# Valid column names
"id", "user_name", "table1.column1", "_private"

# Invalid (rejected)
"id; DROP TABLE", "id OR 1=1", "id'", "123column"
```

#### Parameterized Queries
All filter values use SQLAlchemy's parameterized queries, which safely escape values and prevent SQL injection.

```python
# Safe - value is parameterized
filters = {"user_id": "123; DROP TABLE"}  # Value is safely escaped
```

#### Query Structure Validation
The `/query` endpoint only accepts SELECT statements and rejects:
- Non-SELECT queries (INSERT, UPDATE, DELETE, DROP, etc.)
- Multiple statements (separated by semicolons)

### 2. Custom Query Endpoint Security

The `/query` endpoint accepts user-provided SQL queries. This is **intentional functionality** but comes with security implications:

**Risk Level:** The base SQL query itself is not fully validated beyond ensuring it's a SELECT statement.

**Recommended Usage:**
1. **Development/Testing:** Use freely for exploring data
2. **Production:** 
   - Place behind authentication/authorization
   - Restrict to trusted users only
   - Consider disabling and using dedicated endpoints instead

**Example Production Configuration:**
```python
# Disable custom query endpoint in production
if not settings.allow_custom_queries:
    app.router.routes = [r for r in app.router.routes if r.path != "/query"]
```

### 3. Dedicated Endpoints (Recommended for Production)

Instead of using the custom `/query` endpoint, create dedicated endpoints with predefined queries:

```python
@app.get("/api/v1/users")
async def get_users(
    page: int = Query(1, ge=1),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    # Predefined, safe query
    base_query = "SELECT id, name, email FROM users"
    
    filters = {}
    if status:
        filters["status"] = status  # Column name is hardcoded, safe
    
    return execute_query_with_pagination(db, base_query, filters, page=page)
```

## Authentication & Authorization

This example does not include authentication. In production, you should:

1. **Add Authentication:**
```python
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/query")
async def execute_custom_query(
    credentials: str = Security(security),
    # ... other parameters
):
    # Validate credentials
    if not validate_token(credentials):
        raise HTTPException(status_code=401, detail="Unauthorized")
    # ... rest of implementation
```

2. **Add Role-Based Access Control:**
```python
def require_role(role: str):
    def role_checker(user = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return role_checker

@app.post("/query")
async def execute_custom_query(
    user = Depends(require_role("admin")),
    # ... other parameters
):
    # Only admins can execute custom queries
    pass
```

## Database Connection Security

### Connection String Security
Database credentials are loaded from environment variables and should never be committed to version control.

**Best Practices:**
1. Use `.env` file (gitignored)
2. Use environment-specific credentials
3. Rotate passwords regularly
4. Use read-only database users when possible

### Connection Pooling
SQLAlchemy's connection pooling is configured with:
- `pool_pre_ping=True`: Validates connections before use
- `pool_recycle=3600`: Recycles connections every hour

## Input Validation

All inputs are validated using Pydantic models:
- Page numbers: Must be >= 1
- Page size: Must be between 1 and 100
- Filters: Column names are validated
- Order by: Column names are validated

## Rate Limiting

Consider adding rate limiting in production:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/query")
@limiter.limit("10/minute")
async def execute_custom_query(...):
    pass
```

## Monitoring & Logging

Implement logging for security events:

```python
import logging

logger = logging.getLogger(__name__)

@app.post("/query")
async def execute_custom_query(sql_query: str, ...):
    logger.info(f"Custom query executed: {sql_query[:100]}")
    # ... implementation
```

## Known Limitations

1. **Custom Query Endpoint:** Accepts user-provided SQL queries by design. Should be restricted in production.

2. **CodeQL Alerts:** Static analysis tools may flag the custom query endpoint as a SQL injection risk. This is expected - the risk is acknowledged and documented.

3. **No Built-in Rate Limiting:** Add your own rate limiting for production use.

4. **No Built-in Authentication:** Add authentication/authorization for production use.

## Security Checklist for Production

- [ ] Enable authentication
- [ ] Add authorization/role-based access control
- [ ] Disable or restrict custom query endpoint
- [ ] Add rate limiting
- [ ] Use HTTPS/TLS
- [ ] Enable audit logging
- [ ] Use read-only database user if possible
- [ ] Implement IP whitelisting if applicable
- [ ] Regular security audits
- [ ] Keep dependencies updated

## Reporting Security Issues

If you discover a security vulnerability, please report it by opening an issue on GitHub with the "security" label.
