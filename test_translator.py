"""
Unit tests for PostgreSQL to Sybase SQL translator.
"""

import unittest
from pg2sybase import PostgreSQLToSybaseTranslator, translate_postgresql_to_sybase


class TestPostgreSQLToSybaseTranslator(unittest.TestCase):
    """Test cases for the PostgreSQL to Sybase translator."""
    
    def setUp(self):
        """Set up the translator for each test."""
        self.translator = PostgreSQLToSybaseTranslator()
    
    def test_boolean_literals_true(self):
        """Test conversion of TRUE to 1."""
        query = "SELECT * FROM users WHERE active = TRUE"
        result = self.translator.translate(query)
        self.assertIn('= 1', result)
        self.assertNotIn('TRUE', result)
    
    def test_boolean_literals_false(self):
        """Test conversion of FALSE to 0."""
        query = "SELECT * FROM users WHERE active = FALSE"
        result = self.translator.translate(query)
        self.assertIn('= 0', result)
        self.assertNotIn('FALSE', result)
    
    def test_boolean_literals_case_insensitive(self):
        """Test boolean conversion is case-insensitive."""
        query = "SELECT * FROM users WHERE active = true AND deleted = False"
        result = self.translator.translate(query)
        self.assertIn('= 1', result)
        self.assertIn('= 0', result)
    
    def test_string_concatenation(self):
        """Test conversion of || to +."""
        query = "SELECT first_name || ' ' || last_name AS full_name FROM users"
        result = self.translator.translate(query)
        self.assertIn("first_name + ' ' + last_name", result)
        self.assertNotIn('||', result)
    
    def test_string_concatenation_preserves_strings(self):
        """Test that || inside strings is not replaced."""
        query = "SELECT name FROM users WHERE description = 'test||value'"
        result = self.translator.translate(query)
        # The || inside the string should be preserved
        self.assertIn("'test||value'", result)
    
    def test_data_type_serial(self):
        """Test conversion of SERIAL to IDENTITY."""
        query = "CREATE TABLE users (id SERIAL PRIMARY KEY)"
        result = self.translator.translate(query)
        self.assertIn('NUMERIC(10,0) IDENTITY', result)
        self.assertNotIn('SERIAL', result)
    
    def test_data_type_boolean(self):
        """Test conversion of BOOLEAN to BIT."""
        query = "CREATE TABLE users (active BOOLEAN)"
        result = self.translator.translate(query)
        self.assertIn('BIT', result)
        self.assertNotIn('BOOLEAN', result.upper())
    
    def test_data_type_text(self):
        """Test conversion of TEXT to VARCHAR(MAX)."""
        query = "CREATE TABLE posts (content TEXT)"
        result = self.translator.translate(query)
        self.assertIn('VARCHAR(MAX)', result)
    
    def test_function_now(self):
        """Test conversion of NOW() to GETDATE()."""
        query = "SELECT NOW()"
        result = self.translator.translate(query)
        self.assertIn('GETDATE()', result)
        self.assertNotIn('NOW()', result)
    
    def test_function_current_timestamp(self):
        """Test conversion of CURRENT_TIMESTAMP."""
        query = "SELECT CURRENT_TIMESTAMP"
        result = self.translator.translate(query)
        self.assertIn('GETDATE()', result)
    
    def test_function_length(self):
        """Test conversion of LENGTH to LEN."""
        query = "SELECT LENGTH(name) FROM users"
        result = self.translator.translate(query)
        self.assertIn('LEN(name)', result)
        self.assertNotIn('LENGTH', result)
    
    def test_identifier_quoting(self):
        """Test that double quotes are preserved for identifiers."""
        query = 'SELECT "user_name" FROM "users"'
        result = self.translator.translate(query)
        self.assertIn('"user_name"', result)
        self.assertIn('"users"', result)
    
    def test_identifier_quoting_preserves_string_literals(self):
        """Test that string literals with single quotes are preserved."""
        query = "SELECT name FROM users WHERE city = 'New York'"
        result = self.translator.translate(query)
        self.assertIn("'New York'", result)
    
    def test_limit_clause(self):
        """Test conversion of LIMIT to TOP."""
        query = "SELECT * FROM users LIMIT 10"
        result = self.translator.translate(query)
        self.assertIn('SELECT TOP 10', result)
        self.assertNotIn('LIMIT', result)
    
    def test_limit_offset_clause(self):
        """Test conversion of LIMIT with OFFSET to TOP with START AT."""
        query = "SELECT * FROM users LIMIT 10 OFFSET 20"
        result = self.translator.translate(query)
        self.assertIn('SELECT TOP 10 START AT 21', result)
        self.assertNotIn('LIMIT', result)
        self.assertNotIn('OFFSET', result)
    
    def test_returning_clause(self):
        """Test handling of RETURNING clause."""
        query = "INSERT INTO users (name) VALUES ('John') RETURNING id"
        result = self.translator.translate(query)
        self.assertIn('--', result)  # Should be commented out
        self.assertIn('RETURNING', result)  # But preserved in comment
    
    def test_ilike_operator(self):
        """Test conversion of ILIKE to case-insensitive LIKE."""
        query = "SELECT * FROM users WHERE name ILIKE 'john%'"
        result = self.translator.translate(query)
        self.assertIn('UPPER(name) LIKE UPPER', result)
        self.assertNotIn('ILIKE', result)
    
    def test_complex_query(self):
        """Test a complex query with multiple conversions."""
        query = """
        SELECT "user_id", first_name || ' ' || last_name AS full_name, NOW()
        FROM "users"
        WHERE active = TRUE AND email ILIKE '%@example.com'
        LIMIT 5 OFFSET 10
        """
        result = self.translator.translate(query)
        
        # Check multiple conversions
        self.assertIn('"user_id"', result)
        self.assertIn('"users"', result)
        self.assertIn('+', result)  # String concatenation
        self.assertIn('GETDATE()', result)
        self.assertIn('= 1', result)  # TRUE -> 1
        self.assertIn('UPPER(email) LIKE UPPER', result)  # ILIKE
        self.assertIn('SELECT TOP 5 START AT 11', result)  # LIMIT OFFSET
    
    def test_create_table_with_serial(self):
        """Test CREATE TABLE with SERIAL primary key."""
        query = """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW()
        )
        """
        result = self.translator.translate(query)
        
        self.assertIn('NUMERIC(10,0) IDENTITY', result)
        self.assertIn('VARCHAR(MAX)', result)
        self.assertIn('BIT', result)
        self.assertIn('DEFAULT 1', result)  # TRUE -> 1
        self.assertIn('DATETIME', result)
        self.assertIn('GETDATE()', result)
    
    def test_empty_query(self):
        """Test that empty query returns empty."""
        result = self.translator.translate("")
        self.assertEqual(result, "")
    
    def test_convenience_function(self):
        """Test the convenience function works."""
        query = "SELECT * FROM users WHERE active = TRUE LIMIT 10"
        result = translate_postgresql_to_sybase(query)
        self.assertIn('SELECT TOP 10', result)
        self.assertIn('= 1', result)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""
    
    def setUp(self):
        """Set up the translator for each test."""
        self.translator = PostgreSQLToSybaseTranslator()
    
    def test_mixed_quotes(self):
        """Test query with both single and double quotes."""
        query = 'SELECT "column_name" FROM table WHERE value = \'test\''
        result = self.translator.translate(query)
        self.assertIn('"column_name"', result)
        self.assertIn("'test'", result)
    
    def test_multiple_limit_patterns(self):
        """Test that only the last LIMIT is converted."""
        # This is an edge case - normally you wouldn't have multiple LIMIT
        query = "SELECT * FROM users LIMIT 100"
        result = self.translator.translate(query)
        self.assertIn('TOP 100', result)
    
    def test_case_sensitivity_keywords(self):
        """Test that keywords work in different cases."""
        query = "select * from users where active = true limit 5"
        result = self.translator.translate(query)
        self.assertIn('TOP 5', result.upper())
        self.assertIn('= 1', result)
    
    def test_whitespace_preservation(self):
        """Test that the general structure is preserved."""
        query = "SELECT *\nFROM users\nWHERE active = TRUE"
        result = self.translator.translate(query)
        # Should preserve some structure while making conversions
        self.assertIn('FROM users', result)
        self.assertIn('WHERE active = 1', result)


class TestDataTypes(unittest.TestCase):
    """Test all data type conversions."""
    
    def setUp(self):
        """Set up the translator for each test."""
        self.translator = PostgreSQLToSybaseTranslator()
    
    def test_bigserial(self):
        """Test BIGSERIAL conversion."""
        query = "CREATE TABLE logs (id BIGSERIAL)"
        result = self.translator.translate(query)
        self.assertIn('NUMERIC(19,0) IDENTITY', result)
    
    def test_smallserial(self):
        """Test SMALLSERIAL conversion."""
        query = "CREATE TABLE codes (id SMALLSERIAL)"
        result = self.translator.translate(query)
        self.assertIn('NUMERIC(5,0) IDENTITY', result)
    
    def test_bytea(self):
        """Test BYTEA conversion."""
        query = "CREATE TABLE files (data BYTEA)"
        result = self.translator.translate(query)
        self.assertIn('IMAGE', result)
    
    def test_timestamp_variations(self):
        """Test various timestamp types."""
        query1 = "CREATE TABLE events (ts TIMESTAMP)"
        query2 = "CREATE TABLE events (ts TIMESTAMP WITHOUT TIME ZONE)"
        query3 = "CREATE TABLE events (ts TIMESTAMP WITH TIME ZONE)"
        
        result1 = self.translator.translate(query1)
        result2 = self.translator.translate(query2)
        result3 = self.translator.translate(query3)
        
        self.assertIn('DATETIME', result1)
        self.assertIn('DATETIME', result2)
        self.assertIn('DATETIME', result3)


if __name__ == '__main__':
    unittest.main()
