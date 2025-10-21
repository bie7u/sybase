"""
Sybase database backend for Django.
"""
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.base.validation import BaseDatabaseValidation
from django.core.exceptions import ImproperlyConfigured

try:
    import pyodbc as Database
except ImportError as e:
    raise ImproperlyConfigured("Error loading pyodbc module: %s" % e)

from django_sybase.client import DatabaseClient
from django_sybase.creation import DatabaseCreation
from django_sybase.features import DatabaseFeatures
from django_sybase.introspection import DatabaseIntrospection
from django_sybase.operations import DatabaseOperations
from django_sybase.schema import DatabaseSchemaEditor


class DatabaseWrapper(BaseDatabaseWrapper):
    """
    Database wrapper for Sybase using pyodbc.
    """
    vendor = 'sybase'
    display_name = 'Sybase'
    
    # Mapping of Field objects to their column types
    data_types = {
        'AutoField': 'int',
        'BigAutoField': 'bigint',
        'BinaryField': 'varbinary(max)',
        'BooleanField': 'bit',
        'CharField': 'varchar(%(max_length)s)',
        'DateField': 'date',
        'DateTimeField': 'datetime',
        'DecimalField': 'numeric(%(max_digits)s, %(decimal_places)s)',
        'DurationField': 'bigint',
        'FileField': 'varchar(%(max_length)s)',
        'FilePathField': 'varchar(%(max_length)s)',
        'FloatField': 'float',
        'IntegerField': 'int',
        'BigIntegerField': 'bigint',
        'IPAddressField': 'varchar(15)',
        'GenericIPAddressField': 'varchar(39)',
        'JSONField': 'text',
        'OneToOneField': 'int',
        'PositiveBigIntegerField': 'bigint',
        'PositiveIntegerField': 'int',
        'PositiveSmallIntegerField': 'smallint',
        'SlugField': 'varchar(%(max_length)s)',
        'SmallAutoField': 'smallint',
        'SmallIntegerField': 'smallint',
        'TextField': 'text',
        'TimeField': 'time',
        'UUIDField': 'uniqueidentifier',
    }
    
    data_type_check_constraints = {
        'PositiveBigIntegerField': '%(column)s >= 0',
        'PositiveIntegerField': '%(column)s >= 0',
        'PositiveSmallIntegerField': '%(column)s >= 0',
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
    
    pattern_esc = r"REPLACE(REPLACE(REPLACE({}, '\\', '\\\\'), '%%', '\%%'), '_', '\_')"
    pattern_ops = {
        'contains': r"LIKE '%%' + {} + '%%'",
        'icontains': r"LIKE '%%' + UPPER({}) + '%%'",
        'startswith': r"LIKE {} + '%%'",
        'istartswith': r"LIKE UPPER({}) + '%%'",
        'endswith': r"LIKE '%%' + {}",
        'iendswith': r"LIKE '%%' + UPPER({})",
    }
    
    Database = Database
    SchemaEditorClass = DatabaseSchemaEditor
    
    client_class = DatabaseClient
    creation_class = DatabaseCreation
    features_class = DatabaseFeatures
    introspection_class = DatabaseIntrospection
    ops_class = DatabaseOperations
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.features = DatabaseFeatures(self)
        self.ops = DatabaseOperations(self)
        self.client = DatabaseClient(self)
        self.creation = DatabaseCreation(self)
        self.introspection = DatabaseIntrospection(self)
        self.validation = BaseDatabaseValidation(self)
    
    def get_connection_params(self):
        """
        Return a dict of parameters suitable for pyodbc connection.
        """
        settings_dict = self.settings_dict
        if not settings_dict['NAME']:
            raise ImproperlyConfigured(
                "settings.DATABASES is improperly configured. "
                "Please supply the NAME value."
            )
        
        conn_params = {
            'database': settings_dict['NAME'],
        }
        
        # Build the connection string
        conn_str_parts = []
        
        # Driver
        driver = settings_dict.get('OPTIONS', {}).get('driver', 'FreeTDS')
        conn_str_parts.append('DRIVER={%s}' % driver)
        
        # Server
        if settings_dict.get('HOST'):
            server = settings_dict['HOST']
            if settings_dict.get('PORT'):
                server = '%s:%s' % (server, settings_dict['PORT'])
            conn_str_parts.append('SERVER=%s' % server)
        
        # Database
        conn_str_parts.append('DATABASE=%s' % settings_dict['NAME'])
        
        # Authentication
        if settings_dict.get('USER'):
            conn_str_parts.append('UID=%s' % settings_dict['USER'])
        if settings_dict.get('PASSWORD'):
            conn_str_parts.append('PWD=%s' % settings_dict['PASSWORD'])
        
        # TDS Version (important for Sybase)
        tds_version = settings_dict.get('OPTIONS', {}).get('tds_version', '5.0')
        conn_str_parts.append('TDS_Version=%s' % tds_version)
        
        # Additional options
        extra_params = settings_dict.get('OPTIONS', {}).get('extra_params', {})
        for key, value in extra_params.items():
            conn_str_parts.append('%s=%s' % (key, value))
        
        conn_params['connection_string'] = ';'.join(conn_str_parts)
        conn_params.update(settings_dict.get('OPTIONS', {}))
        
        return conn_params
    
    def get_new_connection(self, conn_params):
        """
        Open a new connection to the database.
        """
        connection_string = conn_params['connection_string']
        connection = Database.connect(connection_string)
        
        # Set autocommit mode
        connection.autocommit = False
        
        return connection
    
    def init_connection_state(self):
        """
        Initialize the connection state.
        """
        # Set any necessary connection options
        pass
    
    def create_cursor(self, name=None):
        """
        Create a cursor for executing queries.
        """
        return self.connection.cursor()
    
    def _set_autocommit(self, autocommit):
        """
        Set the autocommit mode.
        """
        with self.wrap_database_errors:
            self.connection.autocommit = autocommit
    
    def _savepoint(self, sid):
        """
        Create a savepoint.
        """
        with self.cursor() as cursor:
            cursor.execute(self.ops.savepoint_create_sql(sid))
    
    def _savepoint_rollback(self, sid):
        """
        Roll back to a savepoint.
        """
        with self.cursor() as cursor:
            cursor.execute(self.ops.savepoint_rollback_sql(sid))
    
    def _savepoint_commit(self, sid):
        """
        Release a savepoint (Sybase doesn't have explicit savepoint commit).
        """
        pass
    
    def _commit(self):
        """
        Commit the current transaction.
        """
        if self.connection is not None:
            with self.wrap_database_errors:
                return self.connection.commit()
    
    def _rollback(self):
        """
        Roll back the current transaction.
        """
        if self.connection is not None:
            with self.wrap_database_errors:
                return self.connection.rollback()
    
    def _close(self):
        """
        Close the connection.
        """
        if self.connection is not None:
            with self.wrap_database_errors:
                return self.connection.close()
    
    def is_usable(self):
        """
        Test if the connection is usable.
        """
        try:
            with self.cursor() as cursor:
                cursor.execute("SELECT 1")
            return True
        except Exception:
            return False
    
    def _nodb_cursor(self):
        """
        Return a cursor for connecting without a database.
        """
        # Create a connection without specifying a database
        settings_dict = self.settings_dict.copy()
        settings_dict['NAME'] = 'master'  # Connect to master database
        
        conn_params = self.get_connection_params()
        connection = self.get_new_connection(conn_params)
        return connection.cursor()
    
    def schema_editor(self, *args, **kwargs):
        """
        Return a new instance of this backend's SchemaEditor.
        """
        return DatabaseSchemaEditor(self, *args, **kwargs)
