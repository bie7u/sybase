"""
SQL compiler for Sybase.
"""
from django.db.models.sql import compiler


class SQLCompiler(compiler.SQLCompiler):
    """
    SQL compiler for Sybase database.
    """
    
    def as_sql(self, with_limits=True, with_col_aliases=False):
        """
        Create the SQL for this query. Return the SQL string and params.
        """
        # Get the base SQL
        result = super().as_sql(with_limits=False, with_col_aliases=with_col_aliases)
        
        if not with_limits:
            return result
        
        sql, params = result
        
        # Handle LIMIT/OFFSET for Sybase
        if self.query.high_mark is not None or self.query.low_mark:
            # Sybase doesn't support LIMIT/OFFSET directly in older versions
            # Use TOP for simple LIMIT queries
            if self.query.low_mark == 0 and self.query.high_mark is not None:
                # Simple TOP query
                limit = self.query.high_mark
                sql = sql.replace('SELECT', 'SELECT TOP %d' % limit, 1)
            elif self.query.high_mark is not None:
                # Need both offset and limit - use ROW_NUMBER() window function
                offset = self.query.low_mark
                limit = self.query.high_mark - self.query.low_mark
                
                # Wrap the query with ROW_NUMBER
                sql = """
                SELECT * FROM (
                    SELECT ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS __row_num__, inner_query.*
                    FROM (%s) inner_query
                ) outer_query
                WHERE __row_num__ > %d AND __row_num__ <= %d
                """ % (sql, offset, offset + limit)
        
        return sql, params


class SQLInsertCompiler(compiler.SQLInsertCompiler, SQLCompiler):
    """
    Insert compiler for Sybase.
    """
    pass


class SQLDeleteCompiler(compiler.SQLDeleteCompiler, SQLCompiler):
    """
    Delete compiler for Sybase.
    """
    pass


class SQLUpdateCompiler(compiler.SQLUpdateCompiler, SQLCompiler):
    """
    Update compiler for Sybase.
    """
    pass


class SQLAggregateCompiler(compiler.SQLAggregateCompiler, SQLCompiler):
    """
    Aggregate compiler for Sybase.
    """
    pass
