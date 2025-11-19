"""
Examples of using the PostgreSQL to Sybase SQL translator.
"""

from pg2sybase import translate_postgresql_to_sybase, PostgreSQLToSybaseTranslator


def example_basic_select():
    """Basic SELECT query with boolean and LIMIT."""
    print("=" * 60)
    print("Example 1: Basic SELECT with boolean and LIMIT")
    print("=" * 60)
    
    postgresql = "SELECT * FROM users WHERE active = TRUE LIMIT 10"
    sybase = translate_postgresql_to_sybase(postgresql)
    
    print(f"PostgreSQL:\n{postgresql}\n")
    print(f"Sybase:\n{sybase}\n")


def example_string_concatenation():
    """String concatenation example."""
    print("=" * 60)
    print("Example 2: String Concatenation")
    print("=" * 60)
    
    postgresql = "SELECT first_name || ' ' || last_name AS full_name FROM users"
    sybase = translate_postgresql_to_sybase(postgresql)
    
    print(f"PostgreSQL:\n{postgresql}\n")
    print(f"Sybase:\n{sybase}\n")


def example_create_table():
    """CREATE TABLE with various data types."""
    print("=" * 60)
    print("Example 3: CREATE TABLE with PostgreSQL types")
    print("=" * 60)
    
    postgresql = """CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    email VARCHAR(255) UNIQUE,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
)"""
    
    sybase = translate_postgresql_to_sybase(postgresql)
    
    print(f"PostgreSQL:\n{postgresql}\n")
    print(f"Sybase:\n{sybase}\n")


def example_limit_offset():
    """LIMIT and OFFSET pagination."""
    print("=" * 60)
    print("Example 4: Pagination with LIMIT and OFFSET")
    print("=" * 60)
    
    postgresql = "SELECT * FROM products ORDER BY price DESC LIMIT 20 OFFSET 40"
    sybase = translate_postgresql_to_sybase(postgresql)
    
    print(f"PostgreSQL:\n{postgresql}\n")
    print(f"Sybase:\n{sybase}\n")


def example_identifier_quoting():
    """Identifier quoting with double quotes."""
    print("=" * 60)
    print("Example 5: Identifier Quoting")
    print("=" * 60)
    
    postgresql = 'SELECT "user_id", "user_name" FROM "user_table"'
    sybase = translate_postgresql_to_sybase(postgresql)
    
    print(f"PostgreSQL:\n{postgresql}\n")
    print(f"Sybase:\n{sybase}\n")


def example_case_insensitive_search():
    """Case-insensitive LIKE with ILIKE."""
    print("=" * 60)
    print("Example 6: Case-Insensitive Search (ILIKE)")
    print("=" * 60)
    
    postgresql = "SELECT * FROM users WHERE email ILIKE '%@gmail.com'"
    sybase = translate_postgresql_to_sybase(postgresql)
    
    print(f"PostgreSQL:\n{postgresql}\n")
    print(f"Sybase:\n{sybase}\n")


def example_complex_query():
    """Complex query with multiple features."""
    print("=" * 60)
    print("Example 7: Complex Query")
    print("=" * 60)
    
    postgresql = """SELECT 
    "user_id",
    first_name || ' ' || last_name AS full_name,
    LENGTH(email) AS email_length,
    NOW() AS query_time
FROM "users"
WHERE active = TRUE 
    AND email ILIKE '%@example.com'
    AND created_at > CURRENT_TIMESTAMP - INTERVAL '30 days'
ORDER BY created_at DESC
LIMIT 5 OFFSET 10"""
    
    sybase = translate_postgresql_to_sybase(postgresql)
    
    print(f"PostgreSQL:\n{postgresql}\n")
    print(f"Sybase:\n{sybase}\n")


def example_insert_with_returning():
    """INSERT with RETURNING clause."""
    print("=" * 60)
    print("Example 8: INSERT with RETURNING")
    print("=" * 60)
    
    postgresql = "INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com') RETURNING id"
    sybase = translate_postgresql_to_sybase(postgresql)
    
    print(f"PostgreSQL:\n{postgresql}\n")
    print(f"Sybase:\n{sybase}\n")
    print("Note: RETURNING is not directly supported in Sybase.")
    print("Use @@IDENTITY or OUTPUT clause instead.\n")


def example_using_class():
    """Using the translator class directly."""
    print("=" * 60)
    print("Example 9: Using the Translator Class")
    print("=" * 60)
    
    translator = PostgreSQLToSybaseTranslator()
    
    queries = [
        "SELECT * FROM users WHERE deleted = FALSE",
        "SELECT RANDOM() AS random_value",
        "SELECT CURRENT_DATE AS today",
    ]
    
    for query in queries:
        result = translator.translate(query)
        print(f"PostgreSQL: {query}")
        print(f"Sybase:     {result}\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("PostgreSQL to Sybase SQL Translator - Examples")
    print("=" * 60 + "\n")
    
    example_basic_select()
    example_string_concatenation()
    example_create_table()
    example_limit_offset()
    example_identifier_quoting()
    example_case_insensitive_search()
    example_complex_query()
    example_insert_with_returning()
    example_using_class()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)
