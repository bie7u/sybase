"""
Database features for Sybase.
"""
from django.db.backends.base.features import BaseDatabaseFeatures


class DatabaseFeatures(BaseDatabaseFeatures):
    """
    Features specific to Sybase database.
    """
    # Sybase supports transactions
    supports_transactions = True
    supports_savepoints = True
    
    # Sybase supports foreign keys
    supports_foreign_keys = True
    
    # Sybase can return IDs from INSERT statements
    can_return_ids_from_bulk_insert = False
    can_return_columns_from_insert = False
    
    # Sybase-specific features
    supports_tablespaces = True
    supports_sequence_reset = False
    can_introspect_foreign_keys = True
    can_introspect_autofield = True
    
    # String operations
    supports_regex_backreferencing = False
    supports_subqueries_in_group_by = False
    
    # Boolean field support
    has_native_boolean_field = False
    supports_boolean_expr_in_select_clause = True
    
    # JSON support
    supports_json_field = False
    
    # Aggregate functions
    supports_aggregate_filter_clause = False
    
    # Timezones
    supports_timezones = False
    
    # Transactions
    can_rollback_ddl = False
    supports_atomic_references_rename = False
    
    # Index features
    supports_expression_indexes = False
    supports_partial_indexes = False
    supports_covering_indexes = False
    
    # Other features
    supports_ignore_conflicts = False
    supports_update_conflicts = False
    supports_paramstyle_pyformat = False
    supports_over_clause = False
    
    # SELECT ... FOR UPDATE
    has_select_for_update = True
    has_select_for_update_nowait = False
    has_select_for_update_skip_locked = False
    has_select_for_update_of = False
    
    # Collations
    supports_collation_on_charfield = False
    supports_collation_on_textfield = False
    
    # NULL ordering
    supports_null_bytes = False
    
    # Explain
    supports_explaining_query_execution = False
    
    # Constraints
    supports_deferrable_unique_constraints = False
    supports_non_deterministic_collations = False
    
    # Misc
    requires_literal_defaults = True
    closed_cursor_error_class = Exception
    greatest_least_ignores_nulls = True
    supports_temporal_subtraction = True
    supports_slicing_ordering_in_compound = False
    create_test_procedure_without_params_sql = None
    create_test_procedure_with_int_param_sql = None
    supports_comments = False
    supports_comments_inline = False
    
    # Date/DateTime formatting
    supports_microsecond_precision = True
    datetime_cast_date_sql = "CAST(%s AS DATE)"
    datetime_cast_time_sql = "CAST(%s AS TIME)"
    datetime_cast_datetime_sql = "CAST(%s AS DATETIME)"
