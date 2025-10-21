"""
Database schema editor for Sybase.
"""
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.models import NOT_PROVIDED


class DatabaseSchemaEditor(BaseDatabaseSchemaEditor):
    """
    Schema editor for Sybase database.
    """
    
    sql_create_table = "CREATE TABLE %(table)s (%(definition)s)"
    sql_rename_table = "sp_rename '%(old_table)s', '%(new_table)s'"
    sql_retablespace_table = "ALTER TABLE %(table)s LOCK DATAROWS ON %(tablespace)s"
    sql_delete_table = "DROP TABLE %(table)s"
    
    sql_create_column = "ALTER TABLE %(table)s ADD %(column)s %(definition)s"
    sql_alter_column = "ALTER TABLE %(table)s ALTER COLUMN %(column)s %(type)s"
    sql_alter_column_type = "ALTER TABLE %(table)s ALTER COLUMN %(column)s %(type)s"
    sql_alter_column_null = "ALTER TABLE %(table)s MODIFY %(column)s %(type)s NULL"
    sql_alter_column_not_null = "ALTER TABLE %(table)s MODIFY %(column)s %(type)s NOT NULL"
    sql_alter_column_default = "ALTER TABLE %(table)s ALTER COLUMN %(column)s SET DEFAULT %(default)s"
    sql_alter_column_no_default = "ALTER TABLE %(table)s ALTER COLUMN %(column)s DROP DEFAULT"
    sql_delete_column = "ALTER TABLE %(table)s DROP COLUMN %(column)s"
    sql_rename_column = "sp_rename '%(table)s.%(old_column)s', '%(new_column)s', 'COLUMN'"
    
    sql_create_check = "ALTER TABLE %(table)s ADD CONSTRAINT %(name)s CHECK (%(check)s)"
    sql_delete_check = "ALTER TABLE %(table)s DROP CONSTRAINT %(name)s"
    
    sql_create_unique = "ALTER TABLE %(table)s ADD CONSTRAINT %(name)s UNIQUE (%(columns)s)"
    sql_delete_unique = "ALTER TABLE %(table)s DROP CONSTRAINT %(name)s"
    
    sql_create_fk = (
        "ALTER TABLE %(table)s ADD CONSTRAINT %(name)s FOREIGN KEY (%(column)s) "
        "REFERENCES %(to_table)s (%(to_column)s)"
    )
    sql_create_inline_fk = None
    sql_delete_fk = "ALTER TABLE %(table)s DROP CONSTRAINT %(name)s"
    
    sql_create_index = "CREATE INDEX %(name)s ON %(table)s (%(columns)s)%(extra)s"
    sql_create_unique_index = "CREATE UNIQUE INDEX %(name)s ON %(table)s (%(columns)s)%(extra)s"
    sql_delete_index = "DROP INDEX %(table)s.%(name)s"
    
    sql_create_pk = "ALTER TABLE %(table)s ADD CONSTRAINT %(name)s PRIMARY KEY (%(columns)s)"
    sql_delete_pk = "ALTER TABLE %(table)s DROP CONSTRAINT %(name)s"
    
    def quote_value(self, value):
        """
        Quote a value for use in SQL.
        """
        if isinstance(value, (bool, int, float)):
            return str(value)
        if value is None or value == '':
            return 'NULL'
        return "'%s'" % str(value).replace("'", "''")
    
    def _alter_column_type_sql(self, model, old_field, new_field, new_type):
        """
        Generate SQL for altering a column's type.
        """
        return (
            (
                self.sql_alter_column_type % {
                    "column": self.quote_name(new_field.column),
                    "type": new_type,
                },
                [],
            ),
            [],
        )
    
    def _alter_field(self, model, old_field, new_field, old_type, new_type,
                     old_db_params, new_db_params, strict=False):
        """
        Alter a field's type, NULL status, default, etc.
        """
        # Skip if nothing changed
        if old_type == new_type and old_field.null == new_field.null:
            if old_field.default == new_field.default:
                return
        
        # Alter the column type
        if old_type != new_type:
            fragment, other_actions = self._alter_column_type_sql(
                model, old_field, new_field, new_type
            )
            self.execute(fragment[0], fragment[1])
        
        # Alter NULL status
        if old_field.null != new_field.null:
            if new_field.null:
                sql = self.sql_alter_column_null % {
                    "table": self.quote_name(model._meta.db_table),
                    "column": self.quote_name(new_field.column),
                    "type": new_type,
                }
            else:
                sql = self.sql_alter_column_not_null % {
                    "table": self.quote_name(model._meta.db_table),
                    "column": self.quote_name(new_field.column),
                    "type": new_type,
                }
            self.execute(sql)
        
        # Alter default
        old_default = self.effective_default(old_field)
        new_default = self.effective_default(new_field)
        if old_default != new_default:
            if new_default is not None:
                sql = self.sql_alter_column_default % {
                    "table": self.quote_name(model._meta.db_table),
                    "column": self.quote_name(new_field.column),
                    "default": self.quote_value(new_default),
                }
                self.execute(sql)
            else:
                sql = self.sql_alter_column_no_default % {
                    "table": self.quote_name(model._meta.db_table),
                    "column": self.quote_name(new_field.column),
                }
                self.execute(sql)
    
    def _create_index_name(self, table_name, column_names, suffix=""):
        """
        Generate a unique name for an index.
        """
        index_name = '%s_%s' % (table_name, '_'.join(column_names))
        if suffix:
            index_name += '_%s' % suffix
        # Sybase has a 30 character limit on index names
        if len(index_name) > 30:
            index_name = index_name[:30]
        return index_name
    
    def add_field(self, model, field):
        """
        Add a field to a model.
        """
        # Special-case for identity fields - can't add them after table creation
        if field.get_internal_type() in ('AutoField', 'BigAutoField', 'SmallAutoField'):
            # Skip adding identity fields to existing tables
            return
        
        super().add_field(model, field)
    
    def remove_field(self, model, field):
        """
        Remove a field from a model.
        """
        # Check for foreign key constraints first
        if field.remote_field:
            fk_names = self._constraint_names(model, [field.column], foreign_key=True)
            for fk_name in fk_names:
                self.execute(self._delete_fk_sql(model, fk_name))
        
        super().remove_field(model, field)
    
    def _delete_fk_sql(self, model, name):
        """
        Generate SQL to delete a foreign key constraint.
        """
        return self.sql_delete_fk % {
            "table": self.quote_name(model._meta.db_table),
            "name": self.quote_name(name),
        }
    
    def column_sql(self, model, field, include_default=False):
        """
        Return the column definition for a field.
        """
        # Get the column's type
        db_params = field.db_parameters(connection=self.connection)
        sql = db_params['type']
        params = []
        
        # Check for identity (auto-increment) fields
        if field.get_internal_type() in ('AutoField', 'BigAutoField', 'SmallAutoField'):
            sql += ' IDENTITY'
        
        # Check for NULL/NOT NULL
        if not field.null:
            sql += ' NOT NULL'
        else:
            sql += ' NULL'
        
        # Check for default value
        if include_default:
            default = self.effective_default(field)
            if default is not None:
                sql += ' DEFAULT %s' % self.quote_value(default)
        
        # Check for unique
        if field.unique:
            sql += ' UNIQUE'
        
        # Check for primary key
        if field.primary_key:
            sql += ' PRIMARY KEY'
        
        # Check for foreign key
        if field.remote_field:
            to_table = field.remote_field.model._meta.db_table
            to_column = field.remote_field.model._meta.pk.column
            sql += ' REFERENCES %s (%s)' % (
                self.quote_name(to_table),
                self.quote_name(to_column),
            )
        
        return sql, params
    
    def effective_default(self, field):
        """
        Return the effective default value for a field.
        """
        if field.has_default():
            default = field.get_default()
            if callable(default):
                default = default()
            return default
        return None
    
    def skip_default(self, field):
        """
        Some backends don't accept default values for certain columns types.
        """
        return False
    
    def prepare_default(self, value):
        """
        Prepare a value for use as a default value in a column.
        """
        return self.quote_value(value)
