"""
PostgreSQL to Sybase SQL Dialect Translator

A library for translating PostgreSQL SQL queries to Sybase ASE SQL dialect.
"""

from .translator import (
    PostgreSQLToSybaseTranslator,
    translate_postgresql_to_sybase,
    translate,
)

__version__ = "0.1.0"
__all__ = [
    "PostgreSQLToSybaseTranslator",
    "translate_postgresql_to_sybase",
    "translate",
]
