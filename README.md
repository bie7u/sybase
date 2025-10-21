# Django Sybase Database Backend

A complete Django database backend for Sybase ASE (Adaptive Server Enterprise).

## Features

- Full Django ORM support for Sybase ASE
- Support for Django 3.2 and later
- Transaction support with savepoints
- Foreign key constraints
- Schema introspection and migrations
- Connection pooling via pyodbc
- Support for common field types

## Installation

### Prerequisites

1. **FreeTDS** - Required for connecting to Sybase from Unix/Linux systems
   ```bash
   # Ubuntu/Debian
   sudo apt-get install freetds-dev freetds-bin
   
   # macOS
   brew install freetds
   
   # CentOS/RHEL
   sudo yum install freetds freetds-devel
   ```

2. **pyodbc** - Python ODBC bridge
   ```bash
   pip install pyodbc
   ```

3. **Django** - Web framework
   ```bash
   pip install Django>=3.2
   ```

### Install django-sybase

```bash
pip install django-sybase
```

Or install from source:

```bash
git clone https://github.com/bie7u/sybase.git
cd sybase
pip install -e .
```

## Configuration

### FreeTDS Configuration

Create or edit `/etc/freetds/freetds.conf` (or `$HOME/.freetds.conf`):

```ini
[sybase_server]
    host = your_sybase_host
    port = 5000
    tds version = 5.0
    client charset = UTF-8
```

### ODBC Configuration (Optional)

If using ODBC, create or edit `/etc/odbc.ini`:

```ini
[sybase_dsn]
Driver = FreeTDS
Description = Sybase ASE Database
Servername = sybase_server
Database = your_database
```

### Django Settings

In your Django `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django_sybase',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'your_sybase_host',
        'PORT': '5000',
        'OPTIONS': {
            'driver': 'FreeTDS',
            'tds_version': '5.0',
            'extra_params': {
                'APP': 'Django Application',
                'CHARSET': 'UTF8',
            }
        }
    }
}
```

### Configuration Options

- **ENGINE**: Must be `'django_sybase'`
- **NAME**: Database name
- **USER**: Database username
- **PASSWORD**: Database password
- **HOST**: Sybase server hostname or IP
- **PORT**: Sybase server port (default: 5000)
- **OPTIONS**:
  - `driver`: ODBC driver name (default: 'FreeTDS')
  - `tds_version`: TDS protocol version (default: '5.0')
  - `extra_params`: Additional connection parameters

## Usage

### Basic Example

```python
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'authors'

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'books'
```

### Running Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Inspect database
python manage.py inspectdb
```

### Querying

```python
# Create
author = Author.objects.create(name='John Doe', email='john@example.com')

# Read
authors = Author.objects.all()
author = Author.objects.get(id=1)
books = Book.objects.filter(author=author)

# Update
author.name = 'Jane Doe'
author.save()

# Delete
author.delete()

# Complex queries
from django.db.models import Q, Count

books = Book.objects.filter(
    Q(price__lt=50) | Q(author__name__icontains='smith')
).order_by('-published_date')

authors_with_books = Author.objects.annotate(
    book_count=Count('book')
).filter(book_count__gt=0)
```

## Field Type Mappings

| Django Field | Sybase Type |
|--------------|-------------|
| AutoField | int IDENTITY |
| BigAutoField | bigint IDENTITY |
| BigIntegerField | bigint |
| BinaryField | varbinary(max) |
| BooleanField | bit |
| CharField | varchar(n) |
| DateField | date |
| DateTimeField | datetime |
| DecimalField | numeric(p,s) |
| DurationField | bigint |
| EmailField | varchar(254) |
| FileField | varchar(n) |
| FilePathField | varchar(n) |
| FloatField | float |
| IntegerField | int |
| GenericIPAddressField | varchar(39) |
| JSONField | text |
| PositiveBigIntegerField | bigint (CHECK >= 0) |
| PositiveIntegerField | int (CHECK >= 0) |
| PositiveSmallIntegerField | smallint (CHECK >= 0) |
| SlugField | varchar(n) |
| SmallAutoField | smallint IDENTITY |
| SmallIntegerField | smallint |
| TextField | text |
| TimeField | time |
| UUIDField | uniqueidentifier |

## Supported Features

### ✅ Supported
- Transactions with savepoints
- Foreign key constraints
- Unique constraints
- Check constraints
- Indexes (including unique indexes)
- Primary keys
- Schema introspection
- Migrations
- SELECT FOR UPDATE (HOLDLOCK)
- Aggregation (COUNT, SUM, AVG, MAX, MIN)
- Date/time functions
- String operations
- Query optimization

### ❌ Not Supported
- Regex lookups (Sybase limitation)
- JSON field queries (no native JSON support)
- Partial indexes
- Expression indexes
- Deferrable constraints
- Sequences (use IDENTITY columns instead)

## Limitations

1. **Identity Columns**: Cannot be added to existing tables via ALTER TABLE
2. **Name Length**: Maximum 30 characters for table/column/index names
3. **Regex**: No native regex support in Sybase
4. **JSON**: Limited JSON support (stored as text)
5. **Timezones**: No native timezone support
6. **LIMIT/OFFSET**: Implemented using ROW_NUMBER() window function

## Testing

To run the test suite:

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run tests
python manage.py test
```

## Troubleshooting

### Connection Issues

1. **Check FreeTDS configuration**:
   ```bash
   tsql -S sybase_server -U username -P password
   ```

2. **Test ODBC connection**:
   ```bash
   isql -v sybase_dsn username password
   ```

3. **Enable Django debug logging**:
   ```python
   LOGGING = {
       'version': 1,
       'handlers': {
           'console': {
               'class': 'logging.StreamHandler',
           },
       },
       'loggers': {
           'django.db.backends': {
               'handlers': ['console'],
               'level': 'DEBUG',
           },
       },
   }
   ```

### Common Errors

**Error: "Data source name not found"**
- Check your ODBC/FreeTDS configuration
- Verify driver name in OPTIONS

**Error: "Unable to connect"**
- Verify HOST and PORT settings
- Check network connectivity to Sybase server
- Verify firewall rules

**Error: "Invalid TDS version"**
- Adjust `tds_version` in OPTIONS
- Try versions: 4.2, 5.0, 7.0, 7.1, 7.2, 7.3, 7.4

**Error: "Login failed"**
- Verify USER and PASSWORD
- Check user permissions in Sybase

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- Issues: https://github.com/bie7u/sybase/issues
- Documentation: https://github.com/bie7u/sybase
- Django Documentation: https://docs.djangoproject.com/

## Credits

Developed by the Django Sybase community.

## Related Projects

- [django-mssql](https://github.com/microsoft/mssql-django) - SQL Server backend for Django
- [django-db2](https://github.com/ibmdb/python-ibmdb-django) - DB2 backend for Django
- [FreeTDS](https://www.freetds.org/) - Open source implementation of TDS protocol