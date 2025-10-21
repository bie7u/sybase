"""
Database operations for Sybase.
"""
from django.conf import settings
from django.db.backends.base.operations import BaseDatabaseOperations
from django.utils import timezone


class DatabaseOperations(BaseDatabaseOperations):
    """
    Database operations specific to Sybase.
    """
    compiler_module = "django_sybase.compiler"
    
    # SQL templates
    integer_field_ranges = {
        'SmallIntegerField': (-32768, 32767),
        'IntegerField': (-2147483648, 2147483647),
        'BigIntegerField': (-9223372036854775808, 9223372036854775807),
        'PositiveSmallIntegerField': (0, 32767),
        'PositiveIntegerField': (0, 2147483647),
        'PositiveBigIntegerField': (0, 9223372036854775807),
    }
    
    cast_char_field_without_max_length = 'varchar(255)'
    cast_data_types = {
        'AutoField': 'int',
        'BigAutoField': 'bigint',
        'CharField': 'varchar(%(max_length)s)',
        'TextField': 'text',
        'IntegerField': 'int',
        'BigIntegerField': 'bigint',
        'SmallIntegerField': 'smallint',
        'PositiveIntegerField': 'int',
        'PositiveSmallIntegerField': 'smallint',
        'DateField': 'date',
        'DateTimeField': 'datetime',
        'TimeField': 'time',
        'DecimalField': 'numeric(%(max_digits)s, %(decimal_places)s)',
        'FloatField': 'float',
        'BooleanField': 'bit',
    }
    
    def cache_key_culling_sql(self):
        """
        Return SQL to get the first cache key greater than n.
        """
        return "SELECT cache_key FROM %s ORDER BY cache_key OFFSET %%s ROWS FETCH FIRST 1 ROW ONLY"
    
    def date_extract_sql(self, lookup_type, field_name):
        """
        Extract date parts using DATEPART function.
        """
        if lookup_type == 'week_day':
            return "DATEPART(weekday, %s)" % field_name
        else:
            return "DATEPART(%s, %s)" % (lookup_type, field_name)
    
    def date_trunc_sql(self, lookup_type, field_name, tzname=None):
        """
        Truncate date to specified precision.
        """
        fields = {
            'year': "DATEADD(year, DATEDIFF(year, 0, %s), 0)",
            'month': "DATEADD(month, DATEDIFF(month, 0, %s), 0)",
            'day': "DATEADD(day, DATEDIFF(day, 0, %s), 0)",
            'hour': "DATEADD(hour, DATEDIFF(hour, 0, %s), 0)",
            'minute': "DATEADD(minute, DATEDIFF(minute, 0, %s), 0)",
            'second': "DATEADD(second, DATEDIFF(second, 0, %s), 0)",
        }
        if lookup_type in fields:
            return fields[lookup_type] % field_name
        else:
            return "CAST(%s AS DATE)" % field_name
    
    def datetime_cast_date_sql(self, field_name, tzname):
        """
        Cast datetime to date.
        """
        return "CAST(%s AS DATE)" % field_name
    
    def datetime_cast_time_sql(self, field_name, tzname):
        """
        Cast datetime to time.
        """
        return "CAST(%s AS TIME)" % field_name
    
    def datetime_extract_sql(self, lookup_type, field_name, tzname):
        """
        Extract datetime parts.
        """
        return self.date_extract_sql(lookup_type, field_name)
    
    def datetime_trunc_sql(self, lookup_type, field_name, tzname):
        """
        Truncate datetime.
        """
        return self.date_trunc_sql(lookup_type, field_name, tzname)
    
    def time_trunc_sql(self, lookup_type, field_name, tzname=None):
        """
        Truncate time.
        """
        fields = {
            'hour': "CAST(DATEADD(hour, DATEDIFF(hour, 0, %s), 0) AS TIME)",
            'minute': "CAST(DATEADD(minute, DATEDIFF(minute, 0, %s), 0) AS TIME)",
            'second': "CAST(DATEADD(second, DATEDIFF(second, 0, %s), 0) AS TIME)",
        }
        if lookup_type in fields:
            return fields[lookup_type] % field_name
        return "CAST(%s AS TIME)" % field_name
    
    def get_db_converters(self, expression):
        """
        Get database converters for the expression.
        """
        converters = super().get_db_converters(expression)
        internal_type = expression.output_field.get_internal_type()
        if internal_type == 'BooleanField':
            converters.append(self.convert_booleanfield_value)
        elif internal_type in ['DateField', 'DateTimeField', 'TimeField']:
            converters.append(self.convert_datefield_value)
        return converters
    
    def convert_booleanfield_value(self, value, expression, connection):
        """
        Convert Sybase bit field to Python boolean.
        """
        if value in (0, 1):
            return bool(value)
        return value
    
    def convert_datefield_value(self, value, expression, connection):
        """
        Convert date/datetime values.
        """
        return value
    
    def deferrable_sql(self):
        """
        Sybase doesn't support deferrable constraints.
        """
        return ""
    
    def fetch_returned_insert_columns(self, cursor, returning_params):
        """
        Fetch returned columns from INSERT.
        """
        return cursor.fetchone()
    
    def for_update_sql(self, nowait=False, skip_locked=False, of=(), no_key=False):
        """
        Return SQL for SELECT ... FOR UPDATE.
        """
        return 'HOLDLOCK'
    
    def last_insert_id(self, cursor, table_name, pk_name):
        """
        Get the last inserted ID.
        """
        cursor.execute("SELECT @@IDENTITY")
        return cursor.fetchone()[0]
    
    def lookup_cast(self, lookup_type, internal_type=None):
        """
        Return the cast to be used in lookups.
        """
        if lookup_type in ('iexact', 'icontains', 'istartswith', 'iendswith'):
            return "UPPER(%s)"
        return "%s"
    
    def max_name_length(self):
        """
        Return the maximum length of table and column names.
        """
        return 30
    
    def no_limit_value(self):
        """
        Return the value to use when there's no limit.
        """
        return None
    
    def pk_default_value(self):
        """
        Return the default value for a primary key.
        """
        return "DEFAULT"
    
    def prep_for_iexact_query(self, x):
        """
        Prepare a value for use in an iexact query.
        """
        return x
    
    def quote_name(self, name):
        """
        Quote a table or column name.
        """
        if name.startswith('"') and name.endswith('"'):
            return name
        return '"%s"' % name
    
    def random_function_sql(self):
        """
        Return SQL for generating a random value.
        """
        return "RAND()"
    
    def regex_lookup(self, lookup_type):
        """
        Sybase doesn't natively support regex, would need custom implementation.
        """
        raise NotImplementedError("Sybase doesn't support regex lookups")
    
    def return_insert_columns(self, fields):
        """
        Return columns to be returned from INSERT.
        """
        return '', ()
    
    def savepoint_create_sql(self, sid):
        """
        Return SQL for creating a savepoint.
        """
        return "SAVE TRANSACTION %s" % self.quote_name(sid)
    
    def savepoint_commit_sql(self, sid):
        """
        Sybase doesn't have explicit savepoint commit.
        """
        return None
    
    def savepoint_rollback_sql(self, sid):
        """
        Return SQL for rolling back to a savepoint.
        """
        return "ROLLBACK TRANSACTION %s" % self.quote_name(sid)
    
    def sequence_reset_sql(self, style, model_list):
        """
        Return SQL for resetting sequences.
        """
        return []
    
    def sql_flush(self, style, tables, *, reset_sequences=False, allow_cascade=False):
        """
        Return SQL statements for flushing tables.
        """
        if not tables:
            return []
        
        sql = []
        for table in tables:
            sql.append('DELETE FROM %s' % self.quote_name(table))
        return sql
    
    def tablespace_sql(self, tablespace, inline=False):
        """
        Return SQL for specifying tablespace.
        """
        if inline:
            return "ON %s" % self.quote_name(tablespace)
        else:
            return "ON %s" % self.quote_name(tablespace)
    
    def adapt_datefield_value(self, value):
        """
        Transform a date value to a database-specific format.
        """
        if value is None:
            return None
        return value.strftime('%Y-%m-%d')
    
    def adapt_datetimefield_value(self, value):
        """
        Transform a datetime value to a database-specific format.
        """
        if value is None:
            return None
        if timezone.is_aware(value):
            value = timezone.make_naive(value, timezone.utc)
        return value.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    def adapt_timefield_value(self, value):
        """
        Transform a time value to a database-specific format.
        """
        if value is None:
            return None
        if timezone.is_aware(value):
            raise ValueError("Sybase backend does not support timezone-aware times.")
        return value.strftime('%H:%M:%S.%f')[:-3]
    
    def adapt_decimalfield_value(self, value, max_digits=None, decimal_places=None):
        """
        Transform a decimal value.
        """
        return value
    
    def adapt_ipaddressfield_value(self, value):
        """
        Transform an IP address value.
        """
        if value:
            return str(value)
        return None
    
    def year_lookup_bounds_for_date_field(self, value, iso_year=False):
        """
        Return a two-elements list with the lower and upper bound for a year lookup.
        """
        first = '%s-01-01'
        second = '%s-12-31'
        return [first % value, second % value]
    
    def year_lookup_bounds_for_datetime_field(self, value, iso_year=False):
        """
        Return a two-elements list with the lower and upper bound for a year lookup.
        """
        first = '%s-01-01 00:00:00'
        second = '%s-12-31 23:59:59.999'
        return [first % value, second % value]
    
    def combine_expression(self, connector, sub_expressions):
        """
        Combine a list of subexpressions into a single expression.
        """
        if connector == '||':
            # Use + for string concatenation in Sybase
            return ' + '.join(sub_expressions)
        return super().combine_expression(connector, sub_expressions)
    
    def conditional_expression_supported_in_where_clause(self, expression):
        """
        Sybase doesn't support conditional expressions in WHERE clause.
        """
        return False
