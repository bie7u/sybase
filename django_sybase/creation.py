"""
Database creation for Sybase.
"""
from django.db.backends.base.creation import BaseDatabaseCreation


class DatabaseCreation(BaseDatabaseCreation):
    """
    Database creation class for Sybase.
    """
    
    def sql_table_creation_suffix(self):
        """
        SQL to append to the end of the test table creation statements.
        """
        suffix = []
        
        # Add tablespace if specified
        test_settings = self.connection.settings_dict.get('TEST', {})
        if test_settings.get('TABLESPACE'):
            suffix.append('ON %s' % self.connection.ops.quote_name(
                test_settings['TABLESPACE']
            ))
        
        return ' '.join(suffix)
    
    def _execute_create_test_db(self, cursor, parameters, keepdb=False):
        """
        Create the test database.
        """
        try:
            if keepdb:
                return
            cursor.execute('CREATE DATABASE %(dbname)s' % parameters)
        except Exception as e:
            if not keepdb:
                raise e
    
    def _destroy_test_db(self, test_database_name, verbosity):
        """
        Destroy the test database.
        """
        with self.connection._nodb_cursor() as cursor:
            cursor.execute("DROP DATABASE %s" % 
                         self.connection.ops.quote_name(test_database_name))
    
    def _clone_test_db(self, suffix, verbosity, keepdb=False):
        """
        Clone the test database.
        """
        source_database_name = self.connection.settings_dict['NAME']
        target_database_name = self.get_test_db_clone_settings(suffix)['NAME']
        
        with self.connection._nodb_cursor() as cursor:
            try:
                if not keepdb:
                    cursor.execute("CREATE DATABASE %s" % 
                                 self.connection.ops.quote_name(target_database_name))
            except Exception:
                if not keepdb:
                    raise
