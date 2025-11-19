# Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/bie7u/sybase.git
cd sybase

# Install dependencies
pip install -r requirements.txt

# Or install the package
pip install -e .
```

## Quick Test

Run the demo:
```bash
python demo.py
```

Run all examples:
```bash
python examples.py
```

Run tests:
```bash
python -m unittest test_translator.py -v
```

## Basic Usage

```python
from pg2sybase import translate_postgresql_to_sybase

# Simple example
postgresql_query = "SELECT * FROM users WHERE active = TRUE LIMIT 10"
sybase_query = translate_postgresql_to_sybase(postgresql_query)
print(sybase_query)
# Output: SELECT TOP 10 * FROM users WHERE active = 1
```

## Common Use Cases

### 1. Convert a simple SELECT query
```python
from pg2sybase import translate

query = "SELECT name FROM users WHERE deleted = FALSE"
result = translate(query)
# Result: SELECT name FROM users WHERE deleted = 0
```

### 2. Convert CREATE TABLE with PostgreSQL types
```python
query = """
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
)
"""
result = translate(query)
# Converts SERIAL → NUMERIC IDENTITY, TEXT → VARCHAR(MAX), etc.
```

### 3. Convert pagination queries
```python
query = "SELECT * FROM orders ORDER BY created_at DESC LIMIT 50 OFFSET 100"
result = translate(query)
# Result: SELECT TOP 50 START AT 101 * FROM orders ORDER BY created_at DESC
```

### 4. Use the translator class
```python
from pg2sybase import PostgreSQLToSybaseTranslator

translator = PostgreSQLToSybaseTranslator()

queries = [
    "SELECT NOW()",
    "SELECT LENGTH(name) FROM users",
    "SELECT first_name || ' ' || last_name FROM users"
]

for query in queries:
    print(f"PostgreSQL: {query}")
    print(f"Sybase:     {translator.translate(query)}")
    print()
```

## What Gets Converted?

### Data Types
- `SERIAL` → `NUMERIC(10,0) IDENTITY`
- `BOOLEAN` → `BIT`
- `TEXT` → `VARCHAR(MAX)`
- `TIMESTAMP` → `DATETIME`

### Functions
- `NOW()` → `GETDATE()`
- `LENGTH()` → `LEN()`
- `CURRENT_TIMESTAMP` → `GETDATE()`

### Operators & Syntax
- `TRUE` → `1`, `FALSE` → `0`
- `||` (string concat) → `+`
- `"identifier"` → `[identifier]`
- `LIMIT n` → `TOP n`
- `LIMIT n OFFSET m` → `TOP n START AT m+1`
- `ILIKE` → `UPPER() LIKE UPPER()`

## Need Help?

Check the README.md for complete documentation including:
- Full conversion reference tables
- Detailed examples
- Known limitations
- Contributing guidelines

## Running Tests

```bash
# Run all tests
python -m unittest test_translator.py -v

# Should see: Ran 29 tests ... OK
```

All tests should pass!
