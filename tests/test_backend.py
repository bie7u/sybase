"""
Basic tests for Django Sybase backend.

Note: These tests only validate basic package structure.
Full integration tests require Django to be installed.
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDjangoSybaseBackend(unittest.TestCase):
    """
    Test Django Sybase backend components.
    """
    
    def test_import_package(self):
        """Test that the package can be imported."""
        import django_sybase
        self.assertIsNotNone(django_sybase)
        self.assertEqual(django_sybase.__version__, '1.0.0')
    
    def test_package_structure(self):
        """Test that all required modules exist."""
        import os
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        django_sybase_path = os.path.join(base_path, 'django_sybase')
        
        required_files = [
            '__init__.py',
            'base.py',
            'features.py',
            'operations.py',
            'client.py',
            'creation.py',
            'introspection.py',
            'schema.py',
            'compiler.py',
        ]
        
        for file_name in required_files:
            file_path = os.path.join(django_sybase_path, file_name)
            self.assertTrue(
                os.path.exists(file_path),
                f"Required file {file_name} does not exist"
            )
    
    def test_setup_file_exists(self):
        """Test that setup.py exists."""
        import os
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        setup_path = os.path.join(base_path, 'setup.py')
        self.assertTrue(os.path.exists(setup_path))


class TestWithDjango(unittest.TestCase):
    """
    Tests that require Django to be installed.
    These tests are skipped if Django is not available.
    """
    
    def setUp(self):
        """Skip tests if Django is not installed."""
        try:
            import django
            self.django_available = True
        except ImportError:
            self.django_available = False
            self.skipTest("Django is not installed")
    
    def test_import_base(self):
        """Test that base module can be imported with Django."""
        from django_sybase import base
        self.assertIsNotNone(base)
        self.assertTrue(hasattr(base, 'DatabaseWrapper'))
    
    def test_import_features(self):
        """Test that features module can be imported with Django."""
        from django_sybase import features
        self.assertIsNotNone(features)
        self.assertTrue(hasattr(features, 'DatabaseFeatures'))
    
    def test_import_operations(self):
        """Test that operations module can be imported with Django."""
        from django_sybase import operations
        self.assertIsNotNone(operations)
        self.assertTrue(hasattr(operations, 'DatabaseOperations'))
    
    def test_import_client(self):
        """Test that client module can be imported with Django."""
        from django_sybase import client
        self.assertIsNotNone(client)
        self.assertTrue(hasattr(client, 'DatabaseClient'))
    
    def test_import_creation(self):
        """Test that creation module can be imported with Django."""
        from django_sybase import creation
        self.assertIsNotNone(creation)
        self.assertTrue(hasattr(creation, 'DatabaseCreation'))
    
    def test_import_introspection(self):
        """Test that introspection module can be imported with Django."""
        from django_sybase import introspection
        self.assertIsNotNone(introspection)
        self.assertTrue(hasattr(introspection, 'DatabaseIntrospection'))
    
    def test_import_schema(self):
        """Test that schema module can be imported with Django."""
        from django_sybase import schema
        self.assertIsNotNone(schema)
        self.assertTrue(hasattr(schema, 'DatabaseSchemaEditor'))
    
    def test_import_compiler(self):
        """Test that compiler module can be imported with Django."""
        from django_sybase import compiler
        self.assertIsNotNone(compiler)
        self.assertTrue(hasattr(compiler, 'SQLCompiler'))
    
    def test_database_wrapper_vendor(self):
        """Test DatabaseWrapper vendor attribute with Django."""
        from django_sybase.base import DatabaseWrapper
        self.assertEqual(DatabaseWrapper.vendor, 'sybase')
        self.assertEqual(DatabaseWrapper.display_name, 'Sybase')
    
    def test_database_wrapper_data_types(self):
        """Test DatabaseWrapper has data types mapping with Django."""
        from django_sybase.base import DatabaseWrapper
        self.assertIsNotNone(DatabaseWrapper.data_types)
        self.assertIn('AutoField', DatabaseWrapper.data_types)
        self.assertIn('CharField', DatabaseWrapper.data_types)
        self.assertIn('IntegerField', DatabaseWrapper.data_types)
        self.assertEqual(DatabaseWrapper.data_types['AutoField'], 'int')
        self.assertEqual(DatabaseWrapper.data_types['IntegerField'], 'int')
    
    def test_database_wrapper_operators(self):
        """Test DatabaseWrapper has operators mapping with Django."""
        from django_sybase.base import DatabaseWrapper
        self.assertIsNotNone(DatabaseWrapper.operators)
        self.assertIn('exact', DatabaseWrapper.operators)
        self.assertIn('gt', DatabaseWrapper.operators)
        self.assertIn('lt', DatabaseWrapper.operators)
    
    def test_database_features_attributes(self):
        """Test DatabaseFeatures has required attributes with Django."""
        from django_sybase.features import DatabaseFeatures
        
        # Create a mock connection
        class MockConnection:
            pass
        
        conn = MockConnection()
        features = DatabaseFeatures(conn)
        
        self.assertTrue(hasattr(features, 'supports_transactions'))
        self.assertTrue(hasattr(features, 'supports_foreign_keys'))
        self.assertTrue(hasattr(features, 'supports_savepoints'))
    
    def test_database_operations_methods(self):
        """Test DatabaseOperations has required methods with Django."""
        from django_sybase.operations import DatabaseOperations
        
        # Create a mock connection
        class MockConnection:
            pass
        
        conn = MockConnection()
        ops = DatabaseOperations(conn)
        
        self.assertTrue(hasattr(ops, 'quote_name'))
        self.assertTrue(hasattr(ops, 'last_insert_id'))
        self.assertTrue(hasattr(ops, 'random_function_sql'))
        self.assertTrue(callable(ops.quote_name))
        
        # Test quote_name
        quoted = ops.quote_name('test_table')
        self.assertEqual(quoted, '"test_table"')
        
        # Test random function
        random_sql = ops.random_function_sql()
        self.assertEqual(random_sql, "RAND()")
    
    def test_database_client_executable(self):
        """Test DatabaseClient has executable name with Django."""
        from django_sybase.client import DatabaseClient
        
        self.assertEqual(DatabaseClient.executable_name, 'isql')
    
    def test_schema_editor_sql_templates(self):
        """Test DatabaseSchemaEditor has SQL templates with Django."""
        from django_sybase.schema import DatabaseSchemaEditor
        
        self.assertTrue(hasattr(DatabaseSchemaEditor, 'sql_create_table'))
        self.assertTrue(hasattr(DatabaseSchemaEditor, 'sql_delete_table'))
        self.assertTrue(hasattr(DatabaseSchemaEditor, 'sql_create_column'))
        self.assertTrue(hasattr(DatabaseSchemaEditor, 'sql_delete_column'))
    
    def test_introspection_data_types_reverse(self):
        """Test DatabaseIntrospection has reverse data types mapping with Django."""
        from django_sybase.introspection import DatabaseIntrospection
        
        # Create a mock connection
        class MockConnection:
            pass
        
        conn = MockConnection()
        introspection = DatabaseIntrospection(conn)
        
        self.assertIsNotNone(introspection.data_types_reverse)
        self.assertIn('int', introspection.data_types_reverse)
        self.assertIn('varchar', introspection.data_types_reverse)
        self.assertEqual(introspection.data_types_reverse['int'], 'IntegerField')
        self.assertEqual(introspection.data_types_reverse['varchar'], 'CharField')


if __name__ == '__main__':
    unittest.main()
