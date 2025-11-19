# PostgreSQL to Sybase SQL Translator

A Python library for translating PostgreSQL SQL queries to Sybase ASE (Adaptive Server Enterprise) SQL dialect.

## Overview

This translator automatically converts PostgreSQL-specific SQL syntax to Sybase-compatible syntax, handling differences in:
- Data types (SERIAL, BOOLEAN, TEXT, etc.)
- Boolean literals (TRUE/FALSE → 1/0)
- String concatenation (|| → +)
- Functions (NOW(), LENGTH(), etc.)
- Pagination (LIMIT/OFFSET → TOP/START AT)
- Identifier quoting (" → [])
- Case-insensitive search (ILIKE)
- And more...

Based on the [sqlalchemy-sybase](https://pypi.org/project/sqlalchemy-sybase/) library patterns.

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from pg2sybase import translate_postgresql_to_sybase

# Simple translation
postgresql_query = "SELECT * FROM users WHERE active = TRUE LIMIT 10"
sybase_query = translate_postgresql_to_sybase(postgresql_query)
print(sybase_query)
# Output: SELECT TOP 10 * FROM users WHERE active = 1
```

## Usage

### Using as a Python Library

```python
from pg2sybase import translate_postgresql_to_sybase

# Translate a query
result = translate_postgresql_to_sybase("SELECT * FROM users WHERE deleted = FALSE")
# Result: SELECT * FROM users WHERE deleted = 0
```

### Using the Command-Line Interface

```bash
# Direct query
python cli.py "SELECT * FROM users WHERE active = TRUE LIMIT 10"

# From file
python cli.py -f input.sql -o output.sql

# From stdin
echo "SELECT NOW()" | python cli.py

# Pipeline
cat queries.sql | python cli.py > sybase_queries.sql
```

### Using the Translator Class

```python
from pg2sybase import PostgreSQLToSybaseTranslator

translator = PostgreSQLToSybaseTranslator()
sybase_query = translator.translate(postgresql_query)
```

## Supported Conversions

### Data Types

| PostgreSQL | Sybase |
|------------|--------|
| SERIAL | NUMERIC(10,0) IDENTITY |
| BIGSERIAL | NUMERIC(19,0) IDENTITY |
| SMALLSERIAL | NUMERIC(5,0) IDENTITY |
| BOOLEAN | BIT |
| TEXT | VARCHAR(MAX) |
| BYTEA | IMAGE |
| TIMESTAMP | DATETIME |

### Functions

| PostgreSQL | Sybase |
|------------|--------|
| NOW() | GETDATE() |
| CURRENT_TIMESTAMP | GETDATE() |
| CURRENT_DATE | CONVERT(DATE, GETDATE()) |
| CURRENT_TIME | CONVERT(TIME, GETDATE()) |
| LENGTH() | LEN() |
| SUBSTR() | SUBSTRING() |
| RANDOM() | RAND() |

### Operators and Syntax

| PostgreSQL | Sybase | Description |
|------------|--------|-------------|
| TRUE | 1 | Boolean true |
| FALSE | 0 | Boolean false |
| \|\| | + | String concatenation |
| "identifier" | [identifier] | Identifier quoting |
| LIMIT n | TOP n | Result limiting |
| LIMIT n OFFSET m | TOP n START AT m+1 (with * in SELECT) | Pagination (Sybase IQ compatible) |
| ILIKE | UPPER() LIKE UPPER() | Case-insensitive match |

**Note on Pagination**: When using `LIMIT ... OFFSET ...` (which translates to `TOP ... START AT ...`), the column list in the SELECT clause is automatically replaced with `*` for Sybase IQ compatibility. Sybase IQ requires that `TOP ... START AT ...` be immediately followed by the column list without table qualifiers, so using `*` ensures compatibility.

## Examples

### Example 1: Basic SELECT with Pagination

```python
postgresql = "SELECT * FROM users WHERE active = TRUE LIMIT 10"
sybase = translate_postgresql_to_sybase(postgresql)
# SELECT TOP 10 * FROM users WHERE active = 1
```

### Example 2: String Concatenation

```python
postgresql = "SELECT first_name || ' ' || last_name AS full_name FROM users"
sybase = translate_postgresql_to_sybase(postgresql)
# SELECT first_name + ' ' + last_name AS full_name FROM users
```

### Example 3: CREATE TABLE

```python
postgresql = """CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
)"""
sybase = translate_postgresql_to_sybase(postgresql)
# CREATE TABLE users (
#     id NUMERIC(10,0) IDENTITY PRIMARY KEY,
#     username VARCHAR(MAX) NOT NULL,
#     active BIT DEFAULT 1,
#     created_at DATETIME DEFAULT GETDATE()
# )
```

### Example 4: Complex Query with Pagination

```python
postgresql = """SELECT 
    "user_id",
    first_name || ' ' || last_name AS full_name,
    LENGTH(email) AS email_length
FROM "users"
WHERE active = TRUE 
    AND email ILIKE '%@example.com'
LIMIT 5 OFFSET 10"""

sybase = translate_postgresql_to_sybase(postgresql)
# SELECT TOP 5 START AT 11 *
# FROM [users]
# WHERE active = 1 
#     AND UPPER(email) LIKE UPPER('%@example.com')
# 
# Note: Column list replaced with * for Sybase IQ compatibility with TOP START AT
```

### Example 5: Sybase IQ Pagination Compatibility

```python
# Sybase IQ has specific requirements for TOP START AT syntax
postgresql = 'SELECT "id", "name" FROM "dba.users" ORDER BY "id" DESC LIMIT 5 OFFSET 1'
sybase = translate_postgresql_to_sybase(postgresql)
# SELECT TOP 5 START AT 2 *
# FROM [dba.users] ORDER BY [id] DESC
# 
# The column list is replaced with * to avoid table-qualified column names
# which are not supported in Sybase IQ with TOP START AT
```

## Running Examples

```bash
python examples.py
```

This will run all example conversions and display the results.

## Testing

Run the test suite:

```bash
python -m unittest test_translator.py -v
```

All tests should pass, covering:
- Boolean literal conversions
- String concatenation
- Data type mappings
- Function conversions
- Identifier quoting
- LIMIT/OFFSET conversion
- ILIKE operator
- Complex queries
- Edge cases

## Limitations

Some PostgreSQL features don't have direct Sybase equivalents:

1. **RETURNING clause**: Not directly supported in Sybase. The translator comments it out with a note. Use `@@IDENTITY` or `OUTPUT` clause instead.

2. **Arrays**: PostgreSQL array types are not supported in Sybase ASE.

3. **JSON**: PostgreSQL JSON/JSONB types require different handling in Sybase.

4. **Advanced date arithmetic**: Some complex date/time operations may need manual adjustment.

5. **CTEs and Window Functions**: While both databases support these, syntax differences may exist in complex cases.

## Contributing

Contributions are welcome! Please:
1. Add tests for new features
2. Ensure all tests pass
3. Follow the existing code style

## License

This project is open source.

## References

- [Sybase ASE Documentation](https://infocenter.sybase.com/)
- [sqlalchemy-sybase](https://pypi.org/project/sqlalchemy-sybase/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)