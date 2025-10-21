# Example Django settings for Sybase backend

# Basic configuration
DATABASES = {
    'default': {
        'ENGINE': 'django_sybase',
        'NAME': 'my_database',
        'USER': 'my_user',
        'PASSWORD': 'my_password',
        'HOST': 'sybase.example.com',
        'PORT': '5000',
        'OPTIONS': {
            'driver': 'FreeTDS',
            'tds_version': '5.0',
        }
    }
}

# Advanced configuration with connection pooling
DATABASES = {
    'default': {
        'ENGINE': 'django_sybase',
        'NAME': 'production_db',
        'USER': 'app_user',
        'PASSWORD': 'secure_password',
        'HOST': '192.168.1.100',
        'PORT': '5000',
        'OPTIONS': {
            'driver': 'FreeTDS',
            'tds_version': '5.0',
            'extra_params': {
                'APP': 'My Django App',
                'CHARSET': 'UTF8',
                'LANGUAGE': 'us_english',
                'PACKETSIZE': '8192',
            }
        },
        'CONN_MAX_AGE': 600,  # Connection pooling
        'AUTOCOMMIT': True,
    }
}

# Multiple databases
DATABASES = {
    'default': {
        'ENGINE': 'django_sybase',
        'NAME': 'main_db',
        'USER': 'app_user',
        'PASSWORD': 'password1',
        'HOST': 'sybase1.example.com',
        'PORT': '5000',
        'OPTIONS': {
            'driver': 'FreeTDS',
            'tds_version': '5.0',
        }
    },
    'reporting': {
        'ENGINE': 'django_sybase',
        'NAME': 'report_db',
        'USER': 'readonly_user',
        'PASSWORD': 'password2',
        'HOST': 'sybase2.example.com',
        'PORT': '5000',
        'OPTIONS': {
            'driver': 'FreeTDS',
            'tds_version': '5.0',
        }
    }
}

# Test database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django_sybase',
        'NAME': 'production_db',
        'USER': 'app_user',
        'PASSWORD': 'password',
        'HOST': 'sybase.example.com',
        'PORT': '5000',
        'OPTIONS': {
            'driver': 'FreeTDS',
            'tds_version': '5.0',
        },
        'TEST': {
            'NAME': 'test_db',
            'CHARSET': 'utf8',
            'TABLESPACE': None,
        }
    }
}
