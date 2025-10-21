# API Documentation

## Base URL

```
http://localhost:8000/api/
```

## Authentication

Currently, the API is open (no authentication required). To add authentication, configure it in `sybase_project/settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

## Response Format

All responses are in JSON format.

### Success Response

```json
{
  "count": 100,
  "next": "http://localhost:8000/api/endpoint/?page=2",
  "previous": null,
  "results": [...]
}
```

### Error Response

```json
{
  "detail": "Error message"
}
```

## Endpoints

### Root Endpoint

```
GET /api/
```

Returns a list of all available endpoints.

**Response:**
```json
{
  "examples": "http://localhost:8000/api/examples/",
  "customers": "http://localhost:8000/api/customers/"
}
```

---

## ExampleTable Endpoints

### List Examples

```
GET /api/examples/
```

Returns a paginated list of examples.

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `page_size` (integer): Number of items per page (default: 10)
- `name` (string): Filter by name (case-insensitive contains)
- `description` (string): Filter by description (case-insensitive contains)
- `is_active` (boolean): Filter by active status
- `created_after` (datetime): Filter by creation date (>=)
- `created_before` (datetime): Filter by creation date (<=)
- `search` (string): Search in name and description
- `ordering` (string): Order by field (prefix with `-` for descending)

**Example Request:**
```bash
curl "http://localhost:8000/api/examples/?is_active=true&ordering=-created_at"
```

**Response:**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/examples/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Example 1",
      "description": "Description of example 1",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "is_active": true
    },
    ...
  ]
}
```

### Get Active Examples

```
GET /api/examples/active/
```

Returns only active examples.

**Response:** Same format as list examples, but filtered for `is_active=true`.

### Create Example

```
POST /api/examples/
```

Creates a new example.

**Request Body:**
```json
{
  "name": "New Example",
  "description": "Description of the new example",
  "is_active": true
}
```

**Response (201 Created):**
```json
{
  "id": 51,
  "name": "New Example",
  "description": "Description of the new example",
  "created_at": "2024-01-20T14:20:00Z",
  "updated_at": "2024-01-20T14:20:00Z",
  "is_active": true
}
```

### Get Example Details

```
GET /api/examples/{id}/
```

Returns details of a specific example.

**Response:**
```json
{
  "id": 1,
  "name": "Example 1",
  "description": "Description of example 1",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "is_active": true
}
```

### Update Example

```
PUT /api/examples/{id}/
```

Updates an entire example (all fields required).

**Request Body:**
```json
{
  "name": "Updated Example",
  "description": "Updated description",
  "is_active": false
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Updated Example",
  "description": "Updated description",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T15:00:00Z",
  "is_active": false
}
```

### Partial Update Example

```
PATCH /api/examples/{id}/
```

Partially updates an example (only specified fields).

**Request Body:**
```json
{
  "is_active": false
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Example 1",
  "description": "Description of example 1",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T15:05:00Z",
  "is_active": false
}
```

### Delete Example

```
DELETE /api/examples/{id}/
```

Deletes an example.

**Response (204 No Content):** Empty response body.

---

## Customer Endpoints

### List Customers

```
GET /api/customers/
```

Returns a paginated list of customers.

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `page_size` (integer): Number of items per page (default: 10)
- `first_name` (string): Filter by first name (case-insensitive contains)
- `last_name` (string): Filter by last name (case-insensitive contains)
- `email` (string): Filter by email (case-insensitive contains)
- `city` (string): Filter by city (case-insensitive contains)
- `country` (string): Filter by country (case-insensitive contains)
- `created_after` (datetime): Filter by creation date (>=)
- `created_before` (datetime): Filter by creation date (<=)
- `search` (string): Search in first_name, last_name, email, city, country
- `ordering` (string): Order by field (prefix with `-` for descending)

**Example Request:**
```bash
curl "http://localhost:8000/api/customers/?city=Warsaw&ordering=last_name"
```

**Response:**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/customers/?page=2",
  "previous": null,
  "results": [
    {
      "customer_id": 1,
      "first_name": "Jan",
      "last_name": "Kowalski",
      "email": "jan.kowalski@example.com",
      "city": "Warsaw",
      "country": "Poland"
    },
    ...
  ]
}
```

### Get Customers Grouped by Country

```
GET /api/customers/by_country/
```

Returns customers grouped by country with counts.

**Response:**
```json
[
  {
    "country": "Poland",
    "count": 150
  },
  {
    "country": "Germany",
    "count": 75
  },
  ...
]
```

### Create Customer

```
POST /api/customers/
```

Creates a new customer.

**Request Body:**
```json
{
  "first_name": "Anna",
  "last_name": "Nowak",
  "email": "anna.nowak@example.com",
  "phone": "+48987654321",
  "address": "ul. Testowa 5",
  "city": "Krakow",
  "country": "Poland"
}
```

**Response (201 Created):**
```json
{
  "customer_id": 101,
  "first_name": "Anna",
  "last_name": "Nowak",
  "full_name": "Anna Nowak",
  "email": "anna.nowak@example.com",
  "phone": "+48987654321",
  "address": "ul. Testowa 5",
  "city": "Krakow",
  "country": "Poland",
  "created_date": "2024-01-20T16:00:00Z"
}
```

### Get Customer Details

```
GET /api/customers/{id}/
```

Returns details of a specific customer.

**Response:**
```json
{
  "customer_id": 1,
  "first_name": "Jan",
  "last_name": "Kowalski",
  "full_name": "Jan Kowalski",
  "email": "jan.kowalski@example.com",
  "phone": "+48123456789",
  "address": "ul. Przykładowa 1",
  "city": "Warsaw",
  "country": "Poland",
  "created_date": "2024-01-15T10:30:00Z"
}
```

### Update Customer

```
PUT /api/customers/{id}/
```

Updates an entire customer record (all fields required).

**Request Body:**
```json
{
  "first_name": "Jan",
  "last_name": "Kowalski",
  "email": "jan.new@example.com",
  "phone": "+48111222333",
  "address": "ul. Nowa 10",
  "city": "Gdansk",
  "country": "Poland"
}
```

### Partial Update Customer

```
PATCH /api/customers/{id}/
```

Partially updates a customer (only specified fields).

**Request Body:**
```json
{
  "email": "jan.updated@example.com",
  "city": "Poznan"
}
```

### Delete Customer

```
DELETE /api/customers/{id}/
```

Deletes a customer.

**Response (204 No Content):** Empty response body.

---

## Common Query Parameters

### Pagination

- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10, max: 100)

**Example:**
```bash
curl "http://localhost:8000/api/customers/?page=2&page_size=25"
```

### Filtering

Filters are specific to each endpoint. See individual endpoint documentation.

**Example:**
```bash
curl "http://localhost:8000/api/customers/?city=Warsaw&country=Poland"
```

### Search

Use the `search` parameter to search across multiple fields.

**Example:**
```bash
curl "http://localhost:8000/api/customers/?search=john"
```

### Ordering

Use the `ordering` parameter to sort results. Prefix with `-` for descending order.

**Example:**
```bash
# Ascending by last name
curl "http://localhost:8000/api/customers/?ordering=last_name"

# Descending by creation date
curl "http://localhost:8000/api/customers/?ordering=-created_date"

# Multiple fields
curl "http://localhost:8000/api/customers/?ordering=country,city,last_name"
```

### Combining Parameters

All parameters can be combined:

**Example:**
```bash
curl "http://localhost:8000/api/customers/?city=Warsaw&search=jan&ordering=-created_date&page=1&page_size=20"
```

---

## Error Codes

### 200 OK
Request successful.

### 201 Created
Resource created successfully.

### 204 No Content
Resource deleted successfully.

### 400 Bad Request
Invalid request data.

```json
{
  "field_name": ["Error message for this field"]
}
```

### 404 Not Found
Resource not found.

```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
Server error.

```json
{
  "detail": "Internal server error."
}
```

---

## Rate Limiting

Currently not implemented. To add rate limiting, configure it in `sybase_project/settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}
```

---

## CORS

To enable CORS for cross-origin requests, install and configure `django-cors-headers`:

```bash
pip install django-cors-headers
```

Add to `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

---

## Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000/api"

# List customers
response = requests.get(f"{BASE_URL}/customers/")
customers = response.json()
print(f"Total customers: {customers['count']}")

# Get customer by ID
response = requests.get(f"{BASE_URL}/customers/1/")
customer = response.json()
print(f"Customer: {customer['full_name']}")

# Create customer
new_customer = {
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "city": "Warsaw",
    "country": "Poland"
}
response = requests.post(f"{BASE_URL}/customers/", json=new_customer)
created = response.json()
print(f"Created customer ID: {created['customer_id']}")

# Update customer
response = requests.patch(
    f"{BASE_URL}/customers/{created['customer_id']}/",
    json={"city": "Krakow"}
)
updated = response.json()
print(f"Updated city: {updated['city']}")

# Delete customer
response = requests.delete(f"{BASE_URL}/customers/{created['customer_id']}/")
print(f"Delete status: {response.status_code}")  # Should be 204

# Search and filter
params = {
    "city": "Warsaw",
    "search": "jan",
    "ordering": "-created_date",
    "page_size": 20
}
response = requests.get(f"{BASE_URL}/customers/", params=params)
filtered = response.json()
print(f"Found {filtered['count']} matching customers")
```

---

## JavaScript Client Example

```javascript
const BASE_URL = 'http://localhost:8000/api';

// List customers
fetch(`${BASE_URL}/customers/`)
  .then(response => response.json())
  .then(data => {
    console.log(`Total customers: ${data.count}`);
    data.results.forEach(customer => {
      console.log(`${customer.first_name} ${customer.last_name}`);
    });
  });

// Create customer
fetch(`${BASE_URL}/customers/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    first_name: 'Test',
    last_name: 'User',
    email: 'test@example.com',
    city: 'Warsaw',
    country: 'Poland'
  })
})
  .then(response => response.json())
  .then(data => console.log(`Created customer ID: ${data.customer_id}`));

// Update customer
fetch(`${BASE_URL}/customers/1/`, {
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    city: 'Krakow'
  })
})
  .then(response => response.json())
  .then(data => console.log(`Updated city: ${data.city}`));

// Delete customer
fetch(`${BASE_URL}/customers/1/`, {
  method: 'DELETE'
})
  .then(response => console.log(`Delete status: ${response.status}`));

// Search with filters
const params = new URLSearchParams({
  city: 'Warsaw',
  search: 'jan',
  ordering: '-created_date',
  page_size: 20
});

fetch(`${BASE_URL}/customers/?${params}`)
  .then(response => response.json())
  .then(data => console.log(`Found ${data.count} customers`));
```

---

## Testing with cURL

### Basic GET
```bash
curl http://localhost:8000/api/customers/
```

### GET with filters
```bash
curl "http://localhost:8000/api/customers/?city=Warsaw&page_size=5"
```

### POST (Create)
```bash
curl -X POST http://localhost:8000/api/customers/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "city": "Warsaw",
    "country": "Poland"
  }'
```

### PATCH (Update)
```bash
curl -X PATCH http://localhost:8000/api/customers/1/ \
  -H "Content-Type: application/json" \
  -d '{"city": "Krakow"}'
```

### DELETE
```bash
curl -X DELETE http://localhost:8000/api/customers/1/
```

---

## See Also

- [README.md](README.md) - Main documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [USAGE.md](USAGE.md) - Usage examples
- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture overview