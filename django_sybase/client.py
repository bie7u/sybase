"""
Database client for Sybase.
"""
from django.db.backends.base.client import BaseDatabaseClient


class DatabaseClient(BaseDatabaseClient):
    """
    Command-line client for Sybase.
    """
    executable_name = 'isql'
    
    @classmethod
    def settings_to_cmd_args_env(cls, settings_dict, parameters):
        """
        Convert settings to command-line arguments for isql.
        """
        args = [cls.executable_name]
        
        # Server name
        if settings_dict.get('HOST'):
            server = settings_dict['HOST']
            if settings_dict.get('PORT'):
                server = f"{server}:{settings_dict['PORT']}"
            args.extend(['-S', server])
        
        # User
        if settings_dict.get('USER'):
            args.extend(['-U', settings_dict['USER']])
        
        # Password
        if settings_dict.get('PASSWORD'):
            args.extend(['-P', settings_dict['PASSWORD']])
        
        # Database
        if settings_dict.get('NAME'):
            args.extend(['-D', settings_dict['NAME']])
        
        args.extend(parameters)
        
        return args, None
