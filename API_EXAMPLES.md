# API Examples

Comprehensive examples of using the Sybase Database API.

## Table of Contents
- [Basic Queries](#basic-queries)
- [Pagination](#pagination)
- [Filtering](#filtering)
- [Ordering](#ordering)
- [Combined Operations](#combined-operations)
- [Error Handling](#error-handling)
- [Client Libraries](#client-libraries)

## Basic Queries

### Simple SELECT

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT id, name, email FROM users"
  }'
```

### SELECT with Specific Columns

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT id, product_name, price FROM products"
  }'
```

### SELECT with WHERE Clause in Base Query

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT * FROM orders WHERE created_at > '\''2024-01-01'\''"
  }'
```

## Pagination

### First Page (Default)

```bash
curl -X POST "http://localhost:8000/query?page=1&page_size=10" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT * FROM customers"
  }'
```

### Specific Page

```bash
curl -X POST "http://localhost:8000/query?page=5&page_size=20" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT * FROM transactions"
  }'
```

### Large Page Size

```bash
curl -X POST "http://localhost:8000/query?page=1&page_size=100" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT id, name FROM products"
  }'
```

### Response with Pagination Info

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 10,
    "total_records": 150,
    "total_pages": 15,
    "has_next": true,
    "has_previous": false
  }
}
```

## Filtering

### Single Filter

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT * FROM users",
    "filters": {
      "status": "active"
    }
  }'
```

### Multiple Filters (AND Logic)

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT * FROM orders",
    "filters": {
      "status": "completed",
      "payment_method": "credit_card",
      "country": "USA"
    }
  }'
```

### Filter with NULL Value

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT * FROM products",
    "filters": {
      "discontinued_at": null
    }
  }'
```

### Filter with Numbers

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT * FROM products",
    "filters": {
      "category_id": 5,
      "in_stock": 1
    }
  }'
```

## Ordering

### Order by Single Column (Descending)

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT * FROM users",
    "order_by": ["created_at DESC"]
  }'
```

### Order by Single Column (Ascending)

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT * FROM products",
    "order_by": ["name ASC"]
  }'
```

### Order by Multiple Columns

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT * FROM employees",
    "order_by": ["department ASC", "salary DESC", "name ASC"]
  }'
```

### Order by with Table Qualification

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT u.id, u.name, o.order_date FROM users u JOIN orders o ON u.id = o.user_id",
    "order_by": ["o.order_date DESC"]
  }'
```

## Combined Operations

### Filter + Order + Paginate

```bash
curl -X POST "http://localhost:8000/query?page=2&page_size=25" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT * FROM products",
    "filters": {
      "category": "electronics",
      "in_stock": 1
    },
    "order_by": ["price DESC", "name ASC"]
  }'
```

### Complex Query with JOIN

```bash
curl -X POST "http://localhost:8000/query?page=1&page_size=50" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT u.id, u.name, u.email, o.total_amount FROM users u LEFT JOIN orders o ON u.id = o.user_id",
    "filters": {
      "u.status": "active"
    },
    "order_by": ["o.total_amount DESC"]
  }'
```

### Aggregate Query with Filtering

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT category, COUNT(*) as count, AVG(price) as avg_price FROM products GROUP BY category",
    "order_by": ["count DESC"]
  }'
```

## Error Handling

### Invalid SQL Query Type

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "DELETE FROM users WHERE id = 1"
  }'
```

**Response:**
```json
{
  "detail": "Only SELECT queries are allowed"
}
```

### Invalid Column Name in Filter

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT * FROM users",
    "filters": {
      "id; DROP TABLE users": 1
    }
  }'
```

**Response:**
```json
{
  "detail": "Invalid query parameters: Invalid SQL identifier: id; DROP TABLE users"
}
```

### Invalid Order By

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "sql_query": "SELECT * FROM users",
    "order_by": ["id OR 1=1 DESC"]
  }'
```

**Response:**
```json
{
  "detail": "Invalid query parameters: Invalid order_by format: id OR 1=1 DESC"
}
```

## Client Libraries

### Python with requests

```python
import requests

def query_database(sql, page=1, page_size=10, filters=None, order_by=None):
    url = "http://localhost:8000/query"
    params = {"page": page, "page_size": page_size}
    body = {
        "sql_query": sql,
        "filters": filters,
        "order_by": order_by
    }
    
    response = requests.post(url, params=params, json=body)
    response.raise_for_status()
    return response.json()

# Example usage
result = query_database(
    sql="SELECT * FROM users",
    filters={"status": "active"},
    order_by=["created_at DESC"],
    page=1,
    page_size=20
)

print(f"Total records: {result['pagination']['total_records']}")
for user in result['data']:
    print(f"  {user['id']}: {user['name']}")
```

### JavaScript with fetch

```javascript
async function queryDatabase(sql, options = {}) {
  const {
    page = 1,
    pageSize = 10,
    filters = null,
    orderBy = null
  } = options;
  
  const url = new URL('http://localhost:8000/query');
  url.searchParams.append('page', page);
  url.searchParams.append('page_size', pageSize);
  
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      sql_query: sql,
      filters: filters,
      order_by: orderBy
    })
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return await response.json();
}

// Example usage
const result = await queryDatabase(
  'SELECT * FROM products',
  {
    page: 1,
    pageSize: 20,
    filters: { category: 'electronics' },
    orderBy: ['price DESC']
  }
);

console.log(`Total: ${result.pagination.total_records}`);
result.data.forEach(product => {
  console.log(`${product.name}: $${product.price}`);
});
```

### Using the Dedicated Endpoints

```bash
# Example endpoint: Get users
curl "http://localhost:8000/api/v1/example/users?page=1&page_size=10&status=active&order_by=id%20DESC"

# Example endpoint: Get products
curl "http://localhost:8000/api/v1/example/products?page=1&page_size=20&category=electronics"
```

## Best Practices

1. **Always use pagination** for large datasets to avoid memory issues
2. **Use filters** instead of WHERE clauses in base query when possible
3. **Specify ORDER BY** explicitly - don't rely on database default ordering
4. **Use dedicated endpoints** in production rather than the generic `/query` endpoint
5. **Handle pagination** in your client to fetch all pages if needed
6. **Cache results** when appropriate to reduce database load
7. **Set reasonable page_size** values (10-100) based on your needs

## Performance Tips

1. **Limit columns**: Only SELECT columns you need
2. **Use indexes**: Ensure filtered columns are indexed in the database
3. **Optimize queries**: Use EXPLAIN PLAN to analyze query performance
4. **Batch operations**: When fetching all data, use larger page sizes
5. **Monitor response times**: Add logging/monitoring to track query performance
