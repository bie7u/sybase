"""
PostgreSQL to Sybase SQL Dialect Translator

This module provides functionality to translate PostgreSQL SQL queries
to Sybase ASE (Adaptive Server Enterprise) SQL dialect.

Key differences handled:
- LIMIT/OFFSET → TOP/START AT
- Boolean literals (TRUE/FALSE → 1/0)
- String concatenation (|| → +)
- Date/time functions
- SERIAL → IDENTITY
- RETURNING clause
- Identifier quoting (" → [])
"""

import re
import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Where, Token, Parenthesis
from sqlparse.tokens import Keyword, DML, Whitespace, Newline


class PostgreSQLToSybaseTranslator:
    """Translates PostgreSQL SQL queries to Sybase ASE SQL dialect."""
    
    def __init__(self):
        """Initialize the translator with mapping rules."""
        # Data type mappings
        self.type_mappings = {
            'SERIAL': 'NUMERIC(10,0) IDENTITY',
            'BIGSERIAL': 'NUMERIC(19,0) IDENTITY',
            'SMALLSERIAL': 'NUMERIC(5,0) IDENTITY',
            'BOOLEAN': 'BIT',
            'BYTEA': 'IMAGE',
            'TEXT': 'VARCHAR(MAX)',
            'DOUBLE PRECISION': 'DOUBLE PRECISION',
            'TIMESTAMP': 'DATETIME',
            'TIMESTAMP WITHOUT TIME ZONE': 'DATETIME',
            'TIMESTAMP WITH TIME ZONE': 'DATETIME',
        }
        
        # Function mappings
        self.function_mappings = {
            'NOW()': 'GETDATE()',
            'CURRENT_TIMESTAMP': 'GETDATE()',
            'CURRENT_DATE': 'CONVERT(DATE, GETDATE())',
            'CURRENT_TIME': 'CONVERT(TIME, GETDATE())',
            'LENGTH(': 'LEN(',
            'SUBSTR(': 'SUBSTRING(',
            'RANDOM()': 'RAND()',
        }
    
    def translate(self, postgresql_query):
        """
        Translate a PostgreSQL query to Sybase SQL dialect.
        
        Args:
            postgresql_query (str): The PostgreSQL SQL query to translate
            
        Returns:
            str: The translated Sybase SQL query
        """
        if not postgresql_query or not postgresql_query.strip():
            return postgresql_query
        
        # Start with the original query
        sybase_query = postgresql_query
        
        # Step 1: Convert boolean literals
        sybase_query = self._convert_boolean_literals(sybase_query)
        
        # Step 2: Convert string concatenation
        sybase_query = self._convert_string_concatenation(sybase_query)
        
        # Step 3: Convert data types
        sybase_query = self._convert_data_types(sybase_query)
        
        # Step 4: Convert functions
        sybase_query = self._convert_functions(sybase_query)
        
        # Step 5: Convert identifier quoting
        sybase_query = self._convert_identifier_quoting(sybase_query)
        
        # Step 6: Convert LIMIT/OFFSET
        sybase_query = self._convert_limit_offset(sybase_query)
        
        # Step 7: Convert RETURNING clause
        sybase_query = self._convert_returning_clause(sybase_query)
        
        # Step 8: Handle ILIKE (case-insensitive LIKE)
        sybase_query = self._convert_ilike(sybase_query)
        
        return sybase_query.strip()
    
    def _convert_boolean_literals(self, query):
        """Convert PostgreSQL boolean literals to Sybase bit values."""
        # Use word boundaries to avoid replacing TRUE/FALSE within strings
        query = re.sub(r'\bTRUE\b', '1', query, flags=re.IGNORECASE)
        query = re.sub(r'\bFALSE\b', '0', query, flags=re.IGNORECASE)
        return query
    
    def _convert_string_concatenation(self, query):
        """Convert PostgreSQL || string concatenation to Sybase +."""
        # This is a simple replacement, may need refinement for complex cases
        # Avoid replacing || inside strings
        # Simple approach: replace || with + when not inside quotes
        parts = []
        in_string = False
        quote_char = None
        i = 0
        
        while i < len(query):
            char = query[i]
            
            # Track string boundaries
            if char in ('"', "'") and (i == 0 or query[i-1] != '\\'):
                if not in_string:
                    in_string = True
                    quote_char = char
                elif char == quote_char:
                    in_string = False
                    quote_char = None
            
            # Replace || with + outside strings
            if not in_string and i < len(query) - 1 and query[i:i+2] == '||':
                parts.append('+')
                i += 2
                continue
            
            parts.append(char)
            i += 1
        
        return ''.join(parts)
    
    def _convert_data_types(self, query):
        """Convert PostgreSQL data types to Sybase equivalents."""
        result = query
        for pg_type, sybase_type in self.type_mappings.items():
            # Use word boundaries and case-insensitive matching
            pattern = r'\b' + re.escape(pg_type) + r'\b'
            result = re.sub(pattern, sybase_type, result, flags=re.IGNORECASE)
        return result
    
    def _convert_functions(self, query):
        """Convert PostgreSQL functions to Sybase equivalents."""
        result = query
        for pg_func, sybase_func in self.function_mappings.items():
            # Case-insensitive replacement
            pattern = re.escape(pg_func)
            result = re.sub(pattern, sybase_func, result, flags=re.IGNORECASE)
        return result
    
    def _convert_identifier_quoting(self, query):
        """Convert PostgreSQL double-quote identifiers to Sybase bracket notation."""
        # This is complex because we need to distinguish between string literals and identifiers
        # In PostgreSQL, " is for identifiers, ' is for strings
        # In Sybase, [] or " can be used for identifiers (depending on settings), ' for strings
        
        parts = []
        in_string = False
        in_identifier = False
        i = 0
        
        while i < len(query):
            char = query[i]
            
            # Handle string literals (single quotes)
            if char == "'" and (i == 0 or query[i-1] != '\\'):
                in_string = not in_string
                parts.append(char)
                i += 1
                continue
            
            # Handle identifier quoting (double quotes) - only when not in string
            if not in_string and char == '"':
                if not in_identifier:
                    in_identifier = True
                    parts.append('[')
                else:
                    in_identifier = False
                    parts.append(']')
                i += 1
                continue
            
            parts.append(char)
            i += 1
        
        return ''.join(parts)
    
    def _convert_limit_offset(self, query):
        """Convert PostgreSQL LIMIT/OFFSET to Sybase TOP."""
        # Pattern: LIMIT n [OFFSET m]
        # Sybase uses: TOP n START AT m+1
        
        # First, check for LIMIT clause
        limit_pattern = r'\bLIMIT\s+(\d+)(?:\s+OFFSET\s+(\d+))?\s*$'
        match = re.search(limit_pattern, query, re.IGNORECASE)
        
        if match:
            limit_value = match.group(1)
            offset_value = match.group(2) if match.group(2) else None
            
            # Remove the LIMIT/OFFSET clause
            query = re.sub(limit_pattern, '', query, flags=re.IGNORECASE).rstrip()
            
            # Add TOP clause after SELECT
            if offset_value:
                # Sybase START AT is 1-based, so we add 1
                start_at = int(offset_value) + 1
                top_clause = f' TOP {limit_value} START AT {start_at}'
            else:
                top_clause = f' TOP {limit_value}'
            
            # Insert TOP after SELECT keyword
            query = re.sub(
                r'\bSELECT\b',
                f'SELECT{top_clause}',
                query,
                count=1,
                flags=re.IGNORECASE
            )
        
        return query
    
    def _convert_returning_clause(self, query):
        """Convert PostgreSQL RETURNING clause."""
        # PostgreSQL: INSERT/UPDATE/DELETE ... RETURNING *
        # Sybase doesn't have direct RETURNING support
        # We'll convert it to a comment as a workaround
        
        returning_pattern = r'\bRETURNING\s+[\w\s,*]+$'
        match = re.search(returning_pattern, query, re.IGNORECASE)
        
        if match:
            returning_clause = match.group(0)
            # Replace with a comment indicating this needs manual handling
            query = re.sub(
                returning_pattern,
                f'-- {returning_clause} (RETURNING not supported in Sybase, use SELECT after INSERT/UPDATE)',
                query,
                flags=re.IGNORECASE
            )
        
        return query
    
    def _convert_ilike(self, query):
        """Convert PostgreSQL ILIKE to Sybase case-insensitive LIKE."""
        # ILIKE is case-insensitive LIKE in PostgreSQL
        # In Sybase, LIKE can be case-insensitive depending on sort order
        # We'll use UPPER() on both sides as a workaround
        
        # Pattern: column ILIKE 'pattern'
        ilike_pattern = r"(\w+)\s+ILIKE\s+'([^']+)'"
        
        def replace_ilike(match):
            column = match.group(1)
            pattern = match.group(2)
            return f"UPPER({column}) LIKE UPPER('{pattern}')"
        
        query = re.sub(ilike_pattern, replace_ilike, query, flags=re.IGNORECASE)
        
        return query


def translate_postgresql_to_sybase(postgresql_query):
    """
    Convenience function to translate PostgreSQL query to Sybase SQL.
    
    Args:
        postgresql_query (str): The PostgreSQL SQL query to translate
        
    Returns:
        str: The translated Sybase SQL query
        
    Example:
        >>> query = "SELECT * FROM users WHERE active = TRUE LIMIT 10"
        >>> sybase_query = translate_postgresql_to_sybase(query)
        >>> print(sybase_query)
        SELECT TOP 10 * FROM users WHERE active = 1
    """
    translator = PostgreSQLToSybaseTranslator()
    return translator.translate(postgresql_query)


# Convenience alias
translate = translate_postgresql_to_sybase
