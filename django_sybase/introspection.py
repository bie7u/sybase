"""
Database introspection for Sybase.
"""
from django.db.backends.base.introspection import (
    BaseDatabaseIntrospection, FieldInfo, TableInfo,
)
from django.db.models import Index


class DatabaseIntrospection(BaseDatabaseIntrospection):
    """
    Introspection class for Sybase database.
    """
    
    data_types_reverse = {
        'int': 'IntegerField',
        'bigint': 'BigIntegerField',
        'smallint': 'SmallIntegerField',
        'tinyint': 'SmallIntegerField',
        'bit': 'BooleanField',
        'decimal': 'DecimalField',
        'numeric': 'DecimalField',
        'money': 'DecimalField',
        'smallmoney': 'DecimalField',
        'float': 'FloatField',
        'real': 'FloatField',
        'datetime': 'DateTimeField',
        'smalldatetime': 'DateTimeField',
        'date': 'DateField',
        'time': 'TimeField',
        'char': 'CharField',
        'varchar': 'CharField',
        'nchar': 'CharField',
        'nvarchar': 'CharField',
        'text': 'TextField',
        'ntext': 'TextField',
        'binary': 'BinaryField',
        'varbinary': 'BinaryField',
        'image': 'BinaryField',
        'uniqueidentifier': 'UUIDField',
    }
    
    def get_table_list(self, cursor):
        """
        Return a list of table and view names in the current database.
        """
        cursor.execute("""
            SELECT name, CASE type 
                WHEN 'U' THEN 't' 
                WHEN 'V' THEN 'v' 
            END as type
            FROM sysobjects 
            WHERE type IN ('U', 'V')
            ORDER BY name
        """)
        return [TableInfo(row[0], row[1]) for row in cursor.fetchall()]
    
    def get_table_description(self, cursor, table_name):
        """
        Return a description of the table with the given name.
        """
        cursor.execute("""
            SELECT 
                c.name as column_name,
                t.name as type_name,
                c.length,
                c.prec,
                c.scale,
                CASE WHEN c.status & 8 = 8 THEN 1 ELSE 0 END as is_nullable,
                CASE WHEN c.status & 128 = 128 THEN 1 ELSE 0 END as is_identity
            FROM syscolumns c
            INNER JOIN systypes t ON c.usertype = t.usertype
            WHERE c.id = OBJECT_ID(?)
            ORDER BY c.colid
        """, [table_name])
        
        return [
            FieldInfo(
                name=row[0],
                type_code=row[1],
                display_size=row[2],
                internal_size=row[2],
                precision=row[3],
                scale=row[4],
                null_ok=bool(row[5]),
                default=None,
                collation=None,
                is_autofield=bool(row[6]),
                is_unsigned=False,
                has_json_constraint=False,
            )
            for row in cursor.fetchall()
        ]
    
    def get_sequences(self, cursor, table_name, table_fields=()):
        """
        Return a list of introspected sequences for table_name.
        Sybase uses identity columns instead of sequences.
        """
        cursor.execute("""
            SELECT c.name
            FROM syscolumns c
            WHERE c.id = OBJECT_ID(?)
            AND c.status & 128 = 128
        """, [table_name])
        
        return [{'table': table_name, 'column': row[0]} 
                for row in cursor.fetchall()]
    
    def get_relations(self, cursor, table_name):
        """
        Return a dictionary of {field_name: (field_name_other_table, other_table)}
        representing all foreign keys in the given table.
        """
        cursor.execute("""
            SELECT 
                COL_NAME(fc.parent_object_id, fc.parent_column_id) as column_name,
                OBJECT_NAME(fc.referenced_object_id) as referenced_table,
                COL_NAME(fc.referenced_object_id, fc.referenced_column_id) as referenced_column
            FROM sys.foreign_key_columns fc
            WHERE OBJECT_NAME(fc.parent_object_id) = ?
        """, [table_name])
        
        return {
            row[0]: (row[2], row[1])
            for row in cursor.fetchall()
        }
    
    def get_key_columns(self, cursor, table_name):
        """
        Return a list of (column_name, referenced_table_name, referenced_column_name)
        for all key columns in the given table.
        """
        cursor.execute("""
            SELECT 
                COL_NAME(fc.parent_object_id, fc.parent_column_id) as column_name,
                OBJECT_NAME(fc.referenced_object_id) as referenced_table,
                COL_NAME(fc.referenced_object_id, fc.referenced_column_id) as referenced_column
            FROM sys.foreign_key_columns fc
            WHERE OBJECT_NAME(fc.parent_object_id) = ?
        """, [table_name])
        
        return [
            tuple(row)
            for row in cursor.fetchall()
        ]
    
    def get_constraints(self, cursor, table_name):
        """
        Retrieve any constraints or keys (unique, pk, fk, check, index)
        across one or more columns.
        """
        constraints = {}
        
        # Primary key
        cursor.execute("""
            SELECT i.name, COL_NAME(ic.object_id, ic.column_id) as column_name
            FROM sys.indexes i
            INNER JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
            WHERE i.is_primary_key = 1
            AND OBJECT_NAME(i.object_id) = ?
        """, [table_name])
        
        for constraint_name, column in cursor.fetchall():
            if constraint_name not in constraints:
                constraints[constraint_name] = {
                    'columns': [],
                    'primary_key': True,
                    'unique': True,
                    'foreign_key': None,
                    'check': False,
                    'index': False,
                }
            constraints[constraint_name]['columns'].append(column)
        
        # Unique constraints
        cursor.execute("""
            SELECT i.name, COL_NAME(ic.object_id, ic.column_id) as column_name
            FROM sys.indexes i
            INNER JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
            WHERE i.is_unique_constraint = 1
            AND OBJECT_NAME(i.object_id) = ?
        """, [table_name])
        
        for constraint_name, column in cursor.fetchall():
            if constraint_name not in constraints:
                constraints[constraint_name] = {
                    'columns': [],
                    'primary_key': False,
                    'unique': True,
                    'foreign_key': None,
                    'check': False,
                    'index': False,
                }
            constraints[constraint_name]['columns'].append(column)
        
        # Foreign keys
        cursor.execute("""
            SELECT 
                fk.name as constraint_name,
                COL_NAME(fc.parent_object_id, fc.parent_column_id) as column_name,
                OBJECT_NAME(fc.referenced_object_id) as referenced_table,
                COL_NAME(fc.referenced_object_id, fc.referenced_column_id) as referenced_column
            FROM sys.foreign_keys fk
            INNER JOIN sys.foreign_key_columns fc ON fk.object_id = fc.constraint_object_id
            WHERE OBJECT_NAME(fk.parent_object_id) = ?
        """, [table_name])
        
        for constraint_name, column, ref_table, ref_column in cursor.fetchall():
            if constraint_name not in constraints:
                constraints[constraint_name] = {
                    'columns': [],
                    'primary_key': False,
                    'unique': False,
                    'foreign_key': (ref_table, ref_column),
                    'check': False,
                    'index': False,
                }
            constraints[constraint_name]['columns'].append(column)
        
        # Indexes
        cursor.execute("""
            SELECT i.name, COL_NAME(ic.object_id, ic.column_id) as column_name
            FROM sys.indexes i
            INNER JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
            WHERE i.is_primary_key = 0 
            AND i.is_unique_constraint = 0
            AND OBJECT_NAME(i.object_id) = ?
        """, [table_name])
        
        for index_name, column in cursor.fetchall():
            if index_name not in constraints:
                constraints[index_name] = {
                    'columns': [],
                    'primary_key': False,
                    'unique': False,
                    'foreign_key': None,
                    'check': False,
                    'index': True,
                }
            constraints[index_name]['columns'].append(column)
        
        return constraints
