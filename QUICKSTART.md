# Quick Start Guide

This guide will help you get started with Django Sybase backend quickly.

## Prerequisites

Before you begin, ensure you have:
- Python 3.8 or higher
- Django 3.2 or higher
- Access to a Sybase ASE database server
- FreeTDS installed (for Unix/Linux/macOS systems)

## Installation

### Step 1: Install FreeTDS

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install freetds-dev freetds-bin
```

**macOS:**
```bash
brew install freetds
```

**CentOS/RHEL:**
```bash
sudo yum install freetds freetds-devel
```

### Step 2: Install Python dependencies

```bash
pip install Django>=3.2
pip install pyodbc>=4.0.0
```

### Step 3: Install django-sybase

```bash
pip install django-sybase
```

Or from source:
```bash
git clone https://github.com/bie7u/sybase.git
cd sybase
pip install -e .
```

## Configuration

### Configure FreeTDS

Edit `/etc/freetds/freetds.conf` (or create `~/.freetds.conf`):

```ini
[my_sybase]
    host = your_sybase_host
    port = 5000
    tds version = 5.0
```

### Configure Django

In your Django project's `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django_sybase',
        'NAME': 'your_database',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'your_sybase_host',
        'PORT': '5000',
        'OPTIONS': {
            'driver': 'FreeTDS',
            'tds_version': '5.0',
        }
    }
}
```

## Create Your First Model

Create a simple Django model in `models.py`:

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'books'
    
    def __str__(self):
        return self.title
```

## Run Migrations

Create and apply migrations:

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations to Sybase database
python manage.py migrate
```

## Use the ORM

Now you can use Django ORM with your Sybase database:

```python
from myapp.models import Book
from datetime import date

# Create
book = Book.objects.create(
    title='Python Programming',
    author='John Doe',
    isbn='9781234567890',
    published_date=date(2025, 1, 1),
    price=49.99
)

# Read
all_books = Book.objects.all()
book = Book.objects.get(isbn='9781234567890')
expensive_books = Book.objects.filter(price__gt=30)

# Update
book.price = 39.99
book.save()

# Delete
book.delete()
```

## Common Operations

### Using the Django Shell

```bash
python manage.py shell
```

```python
>>> from myapp.models import Book
>>> Book.objects.count()
5
>>> Book.objects.filter(author__icontains='doe')
<QuerySet [<Book: Python Programming>]>
```

### Inspecting Existing Database

If you have an existing Sybase database:

```bash
python manage.py inspectdb > models.py
```

This generates Django model code from your existing database schema.

### Running Queries

```python
from django.db.models import Q, Count, Avg

# Complex queries
books = Book.objects.filter(
    Q(price__lt=50) | Q(author__icontains='smith')
).order_by('-published_date')

# Aggregation
avg_price = Book.objects.aggregate(Avg('price'))
print(f"Average price: ${avg_price['price__avg']:.2f}")

# Count by author
from django.db.models import Count
author_counts = Book.objects.values('author').annotate(
    count=Count('id')
).order_by('-count')
```

## Testing Your Connection

Create a simple test script `test_connection.py`:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.db import connection

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT @@version")
        version = cursor.fetchone()
        print(f"Connected to Sybase: {version[0]}")
except Exception as e:
    print(f"Connection failed: {e}")
```

Run it:
```bash
python test_connection.py
```

## Troubleshooting

### Problem: Cannot connect to Sybase

**Solution:**
1. Verify Sybase server is running: `telnet your_host 5000`
2. Check FreeTDS configuration: `tsql -S my_sybase -U username -P password`
3. Verify firewall allows connection on port 5000

### Problem: Login failed

**Solution:**
1. Verify username and password in settings
2. Check user has permissions: `sp_displaylogin 'username'` in Sybase
3. Ensure database exists: `SELECT name FROM sysdatabases`

### Problem: TDS version mismatch

**Solution:**
Try different TDS versions in OPTIONS:
```python
'OPTIONS': {
    'tds_version': '5.0',  # Try: 4.2, 5.0, 7.0, 7.1, 7.2, 7.3, 7.4
}
```

### Problem: Character encoding issues

**Solution:**
Add charset to OPTIONS:
```python
'OPTIONS': {
    'extra_params': {
        'CHARSET': 'UTF8',
    }
}
```

## Next Steps

- Read the full [README](README.md) for detailed documentation
- Check out [example models](examples/models.py) for more complex scenarios
- Review [Django database documentation](https://docs.djangoproject.com/en/stable/ref/databases/)
- Learn about [Django migrations](https://docs.djangoproject.com/en/stable/topics/migrations/)

## Getting Help

- Issues: https://github.com/bie7u/sybase/issues
- Django Forums: https://forum.djangoproject.com/
- Stack Overflow: Tag your questions with `django` and `sybase`

## Example Project Structure

```
myproject/
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings.py      # Configure database here
│   ├── urls.py
│   └── wsgi.py
├── myapp/
│   ├── __init__.py
│   ├── models.py        # Define your models
│   ├── views.py
│   ├── admin.py
│   └── migrations/
│       └── __init__.py
└── requirements.txt
```

## Sample requirements.txt

```
Django>=3.2
pyodbc>=4.0.0
django-sybase>=1.0.0
```

Congratulations! You're now ready to use Django with Sybase ASE. Happy coding! 🎉
