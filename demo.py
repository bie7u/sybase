#!/usr/bin/env python3
"""
Quick demo script for PostgreSQL to Sybase SQL translator.
Run this to see the translator in action.
"""

from pg2sybase import translate_postgresql_to_sybase

def main():
    print("=" * 70)
    print("PostgreSQL to Sybase SQL Translator - Quick Demo")
    print("=" * 70)
    print()
    
    # Example queries
    examples = [
        ("Basic SELECT with LIMIT", 
         "SELECT * FROM users WHERE active = TRUE LIMIT 10"),
        
        ("String concatenation",
         "SELECT first_name || ' ' || last_name FROM users"),
        
        ("CREATE TABLE with PostgreSQL types",
         "CREATE TABLE users (id SERIAL, name TEXT, active BOOLEAN)"),
        
        ("Pagination with OFFSET",
         "SELECT * FROM products LIMIT 20 OFFSET 40"),
        
        ("Case-insensitive search",
         "SELECT * FROM users WHERE email ILIKE '%@gmail.com'"),
    ]
    
    for title, pg_query in examples:
        print(f"Example: {title}")
        print("-" * 70)
        print(f"PostgreSQL: {pg_query}")
        sybase_query = translate_postgresql_to_sybase(pg_query)
        print(f"Sybase:     {sybase_query}")
        print()
    
    print("=" * 70)
    print("Try it yourself!")
    print("=" * 70)
    print()
    print("from pg2sybase import translate_postgresql_to_sybase")
    print("result = translate_postgresql_to_sybase(your_postgresql_query)")
    print()

if __name__ == "__main__":
    main()
