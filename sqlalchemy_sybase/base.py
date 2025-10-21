"""
Sybase database backend using SQLAlchemy.

This backend provides Django ORM support for Sybase databases through SQLAlchemy.
"""
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.base.features import BaseDatabaseFeatures
from django.db.backends.base.operations import BaseDatabaseOperations
from django.db.backends.base.client import BaseDatabaseClient
from django.db.backends.base.creation import BaseDatabaseCreation
from django.db.backends.base.introspection import BaseDatabaseIntrospection
from django.db.backends.base.validation import BaseDatabaseValidation

from sqlalchemy import create_engine, event
from sqlalchemy.pool import NullPool
import pyodbc


class DatabaseFeatures(BaseDatabaseFeatures):
    """Database features for Sybase."""
    supports_transactions = True
    can_use_chunked_reads = True
    can_return_columns_from_insert = False
    has_bulk_insert = True
    uses_savepoints = True
    supports_tablespaces = True
    supports_sequence_reset = False
    can_introspect_autofield = True
    can_introspect_big_integer_field = True
    can_introspect_binary_field = False
    can_introspect_decimal_field = True
    can_introspect_duration_field = False
    can_introspect_small_integer_field = True
    can_introspect_positive_integer_field = False
    supports_timezones = False
    supports_regex_backreferencing = False
    supports_subqueries_in_group_by = False


class DatabaseOperations(BaseDatabaseOperations):
    """Database operations for Sybase."""
    compiler_module = "django.db.backends.sqlite3.compiler"
    
    def quote_name(self, name):
        """Quote table and column names."""
        if name.startswith('"') and name.endswith('"'):
            return name
        return '"%s"' % name
    
    def sql_flush(self, style, tables, sequences, allow_cascade=False):
        """Return SQL statements to flush tables."""
        if tables:
            sql = ['DELETE FROM %s;' % self.quote_name(table) for table in tables]
            return sql
        return []


class DatabaseClient(BaseDatabaseClient):
    """Database client for Sybase."""
    executable_name = 'isql'


class DatabaseCreation(BaseDatabaseCreation):
    """Database creation for Sybase."""
    pass


class DatabaseIntrospection(BaseDatabaseIntrospection):
    """Database introspection for Sybase."""
    
    def get_table_list(self, cursor):
        """Return list of table names in the database."""
        cursor.execute("""
            SELECT name FROM sysobjects 
            WHERE type='U' 
            ORDER BY name
        """)
        return [row[0] for row in cursor.fetchall()]


class DatabaseValidation(BaseDatabaseValidation):
    """Database validation for Sybase."""
    pass


class DatabaseWrapper(BaseDatabaseWrapper):
    """
    Database wrapper for Sybase using SQLAlchemy.
    """
    vendor = 'sybase'
    display_name = 'Sybase'
    
    data_types = {
        'AutoField': 'int identity',
        'BigAutoField': 'bigint identity',
        'BinaryField': 'varbinary(max)',
        'BooleanField': 'bit',
        'CharField': 'varchar(%(max_length)s)',
        'DateField': 'date',
        'DateTimeField': 'datetime',
        'DecimalField': 'numeric(%(max_digits)s, %(decimal_places)s)',
        'DurationField': 'bigint',
        'FileField': 'varchar(100)',
        'FilePathField': 'varchar(100)',
        'FloatField': 'float',
        'IntegerField': 'int',
        'BigIntegerField': 'bigint',
        'IPAddressField': 'varchar(15)',
        'GenericIPAddressField': 'varchar(39)',
        'OneToOneField': 'int',
        'PositiveIntegerField': 'int',
        'PositiveSmallIntegerField': 'smallint',
        'SlugField': 'varchar(%(max_length)s)',
        'SmallIntegerField': 'smallint',
        'TextField': 'text',
        'TimeField': 'time',
        'UUIDField': 'uniqueidentifier',
    }
    
    operators = {
        'exact': '= %s',
        'iexact': "= UPPER(%s)",
        'contains': "LIKE %s",
        'icontains': "LIKE UPPER(%s)",
        'gt': '> %s',
        'gte': '>= %s',
        'lt': '< %s',
        'lte': '<= %s',
        'startswith': "LIKE %s",
        'endswith': "LIKE %s",
        'istartswith': "LIKE UPPER(%s)",
        'iendswith': "LIKE UPPER(%s)",
    }
    
    Database = pyodbc
    SchemaEditorClass = None
    
    features_class = DatabaseFeatures
    ops_class = DatabaseOperations
    client_class = DatabaseClient
    creation_class = DatabaseCreation
    introspection_class = DatabaseIntrospection
    validation_class = DatabaseValidation
    
    def __init__(self, settings_dict, alias=None):
        super().__init__(settings_dict, alias)
        self.sqlalchemy_engine = None
    
    def get_connection_params(self):
        """Return connection parameters for the database."""
        settings_dict = self.settings_dict
        
        # Build connection string for Sybase
        conn_params = {
            'server': settings_dict.get('HOST', 'localhost'),
            'port': settings_dict.get('PORT', '5000'),
            'database': settings_dict.get('NAME', ''),
            'user': settings_dict.get('USER', ''),
            'password': settings_dict.get('PASSWORD', ''),
        }
        
        options = settings_dict.get('OPTIONS', {})
        conn_params.update(options)
        
        return conn_params
    
    def get_new_connection(self, conn_params):
        """Create a new database connection."""
        # Build SQLAlchemy connection string
        server = conn_params.get('server', 'localhost')
        port = conn_params.get('port', '5000')
        database = conn_params.get('database', '')
        user = conn_params.get('user', '')
        password = conn_params.get('password', '')
        driver = conn_params.get('driver', 'FreeTDS')
        
        # Build connection string
        # Format: sybase+pyodbc://user:password@host:port/database?driver=FreeTDS
        conn_str = f"sybase+pyodbc://{user}:{password}@{server}:{port}/{database}?driver={driver}"
        
        # Create SQLAlchemy engine
        if not self.sqlalchemy_engine:
            self.sqlalchemy_engine = create_engine(
                conn_str,
                poolclass=NullPool,
                echo=False
            )
        
        # Get raw connection from SQLAlchemy
        connection = self.sqlalchemy_engine.raw_connection()
        
        return connection
    
    def init_connection_state(self):
        """Initialize the database connection settings."""
        pass
    
    def create_cursor(self, name=None):
        """Create a cursor for executing queries."""
        return self.connection.cursor()
    
    def _set_autocommit(self, autocommit):
        """Set autocommit mode."""
        with self.wrap_database_errors:
            self.connection.autocommit = autocommit
    
    def is_usable(self):
        """Check if the connection is still usable."""
        try:
            self.connection.cursor()
            return True
        except Exception:
            return False
