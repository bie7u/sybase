# Architektura Aplikacji Django Sybase

## Przegląd

Aplikacja Django łącząca się z bazą danych Sybase poprzez SQLAlchemy, z API REST zbudowanym w Django REST Framework.

## Schemat architektury

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client (Browser/App)                     │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTP Requests
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Django Application                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                     URLs (sybase_project/urls.py)         │  │
│  │                            ↓                              │  │
│  │                     API Router (api/urls.py)              │  │
│  └──────────────────────────┬────────────────────────────────┘  │
│                             ↓                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Django REST Framework (DRF)                   │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  ViewSets (api/views.py)                           │  │  │
│  │  │  - ExampleTableViewSet                             │  │  │
│  │  │  - CustomerViewSet                                 │  │  │
│  │  │    ↓                                                │  │  │
│  │  │  Serializers (api/serializers.py)                 │  │  │
│  │  │  - ExampleTableSerializer                          │  │  │
│  │  │  - CustomerSerializer                              │  │  │
│  │  │    ↓                                                │  │  │
│  │  │  Filters (api/filters.py)                         │  │  │
│  │  │  - ExampleTableFilter                              │  │  │
│  │  │  - CustomerFilter                                  │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────┬────────────────────────────────┘  │
│                             ↓                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Django ORM                             │  │
│  │                    Models (api/models.py)                 │  │
│  │                    - ExampleTable                         │  │
│  │                    - Customer                             │  │
│  └──────────────────────────┬────────────────────────────────┘  │
│                             ↓                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │        Database Backend (sqlalchemy_sybase/base.py)       │  │
│  │        - DatabaseWrapper                                  │  │
│  │        - DatabaseOperations                               │  │
│  │        - DatabaseFeatures                                 │  │
│  └──────────────────────────┬────────────────────────────────┘  │
└────────────────────────────┬┬────────────────────────────────────┘
                             ││
        ┌────────────────────┘└────────────────────┐
        ↓                                           ↓
┌────────────────┐                          ┌────────────────┐
│  SQLAlchemy    │                          │   PyODBC       │
└───────┬────────┘                          └───────┬────────┘
        └─────────────────┬─────────────────────────┘
                          ↓
                  ┌───────────────┐
                  │    FreeTDS    │
                  └───────┬───────┘
                          ↓
                  ┌───────────────┐
                  │ Sybase Server │
                  └───────────────┘
```

## Komponenty

### 1. Warstwa prezentacji (DRF)

**Lokalizacja:** `api/views.py`

**Odpowiedzialność:**
- Obsługa żądań HTTP
- Walidacja danych wejściowych
- Formatowanie odpowiedzi
- Paginacja wyników
- Filtrowanie i wyszukiwanie
- Autoryzacja (jeśli włączona)

**ViewSets:**
- `ExampleTableViewSet` - CRUD dla tabeli przykładowej
- `CustomerViewSet` - CRUD dla tabeli klientów

### 2. Warstwa serializacji

**Lokalizacja:** `api/serializers.py`

**Odpowiedzialność:**
- Konwersja modeli Django na JSON
- Walidacja danych wejściowych
- Obsługa zagnieżdżonych relacji
- Dodatkowe pola wyliczane (np. full_name)

**Serializery:**
- `ExampleTableSerializer` - Pełny serializer
- `CustomerSerializer` - Pełny serializer z dodatkowymi polami
- `CustomerListSerializer` - Lekki serializer dla list

### 3. Warstwa filtrowania

**Lokalizacja:** `api/filters.py`

**Odpowiedzialność:**
- Definiowanie kryteriów filtrowania
- Mapowanie parametrów URL na zapytania
- Obsługa różnych typów filtrów (exact, contains, date ranges)

**Filtry:**
- `ExampleTableFilter` - Filtry dla ExampleTable
- `CustomerFilter` - Filtry dla Customer

### 4. Warstwa modeli (Django ORM)

**Lokalizacja:** `api/models.py`

**Odpowiedzialność:**
- Mapowanie tabel bazy danych na obiekty Python
- Definiowanie relacji między tabelami
- Walidacja na poziomie modelu
- Meta informacje (nazwa tabeli, indeksy, itp.)

**Modele:**
- `ExampleTable` - Przykładowa tabela
- `Customer` - Tabela klientów

**Ważne:** Wszystkie modele mają `managed = False`, co oznacza, że Django nie będzie tworzyć/modyfikować tabel.

### 5. Warstwa dostępu do danych (Database Backend)

**Lokalizacja:** `sqlalchemy_sybase/base.py`

**Odpowiedzialność:**
- Implementacja interfejsu Django database backend
- Tłumaczenie zapytań Django ORM na SQL Sybase
- Zarządzanie połączeniami
- Obsługa transakcji

**Komponenty:**
- `DatabaseWrapper` - Główna klasa wrappera
- `DatabaseOperations` - Operacje specyficzne dla Sybase
- `DatabaseFeatures` - Funkcjonalności bazy danych
- `DatabaseIntrospection` - Introspekcja schematu

### 6. Warstwa połączenia

**SQLAlchemy:**
- Zarządza pool połączeń
- Tworzy connection string
- Obsługuje sesje

**PyODBC:**
- Sterownik ODBC dla Python
- Komunikacja z FreeTDS

**FreeTDS:**
- Implementacja protokołu TDS
- Komunikacja z Sybase Server

## Przepływ danych

### GET Request (Odczyt)

```
1. Client → GET /api/customers/?city=Warsaw
2. Django URLs → API Router → CustomerViewSet.list()
3. ViewSet → CustomerFilter.filter_queryset()
4. Filter → Django ORM Query
5. ORM → DatabaseWrapper
6. DatabaseWrapper → SQLAlchemy → PyODBC → FreeTDS
7. FreeTDS → Sybase Server (SELECT * FROM customers WHERE city='Warsaw')
8. Sybase → Wyniki → FreeTDS → PyODBC → SQLAlchemy
9. SQLAlchemy → DatabaseWrapper → ORM Objects
10. ORM Objects → CustomerSerializer
11. Serializer → JSON
12. JSON → Paginacja → Response
13. Response → Client
```

### POST Request (Zapis)

```
1. Client → POST /api/customers/ + JSON data
2. Django URLs → API Router → CustomerViewSet.create()
3. ViewSet → CustomerSerializer.is_valid()
4. Serializer → Walidacja danych
5. Serializer → CustomerSerializer.save()
6. Save → Django ORM .create()
7. ORM → DatabaseWrapper
8. DatabaseWrapper → SQLAlchemy → PyODBC → FreeTDS
9. FreeTDS → Sybase Server (INSERT INTO customers ...)
10. Sybase → Potwierdzenie → FreeTDS → PyODBC → SQLAlchemy
11. SQLAlchemy → DatabaseWrapper → Nowy obiekt ORM
12. ORM Object → CustomerSerializer
13. Serializer → JSON (201 Created)
14. JSON → Client
```

## Konfiguracja

### settings.py

```python
# Wybór bazy danych
USE_SYBASE = True/False

# Jeśli USE_SYBASE = True:
DATABASES = {
    'default': {
        'ENGINE': 'sqlalchemy_sybase.base',  # Nasz custom backend
        'NAME': 'database_name',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'hostname',
        'PORT': '5000',
    }
}

# DRF Configuration
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

## Rozszerzalność

### Dodawanie nowych endpointów

1. **Model** (`api/models.py`):
```python
class NewTable(models.Model):
    # pola...
    class Meta:
        managed = False
        db_table = 'existing_table_name'
```

2. **Serializer** (`api/serializers.py`):
```python
class NewTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewTable
        fields = '__all__'
```

3. **Filter** (`api/filters.py`):
```python
class NewTableFilter(django_filters.FilterSet):
    class Meta:
        model = NewTable
        fields = ['field1', 'field2']
```

4. **ViewSet** (`api/views.py`):
```python
class NewTableViewSet(viewsets.ModelViewSet):
    queryset = NewTable.objects.all()
    serializer_class = NewTableSerializer
    filterset_class = NewTableFilter
```

5. **URL** (`api/urls.py`):
```python
router.register(r'newtable', NewTableViewSet, basename='newtable')
```

## Bezpieczeństwo

### Warstwy bezpieczeństwa:

1. **Django Security Middleware**
   - CSRF Protection
   - XSS Protection
   - Clickjacking Protection

2. **DRF Authentication** (do konfiguracji)
   - Token Authentication
   - Session Authentication
   - JWT

3. **Database Level**
   - Parametryzowane zapytania (SQL injection protection)
   - User permissions w bazie danych

4. **Network Level**
   - HTTPS (produkcja)
   - VPN/Firewall rules

## Monitoring i Logging

### Django Logging
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

### Metryki do monitorowania:
- Czas odpowiedzi API
- Liczba zapytań do bazy
- Błędy połączenia
- Cache hit/miss ratio

## Performance

### Optymalizacje:

1. **Database Level**
   - Indeksy w Sybase
   - Query optimization
   - Connection pooling (SQLAlchemy)

2. **Django Level**
   - `select_related()` / `prefetch_related()`
   - Django cache framework
   - Pagination

3. **DRF Level**
   - Lightweight serializers dla list
   - Response caching
   - Throttling

## Skalowanie

### Horizontal Scaling:
- Wiele instancji Django
- Load balancer
- Shared cache (Redis/Memcached)

### Vertical Scaling:
- Więcej CPU/RAM
- Optymalizacja connection pool
- Async workers (Celery)

## Testowanie

### Typy testów:
1. **Unit Tests** - Pojedyncze komponenty
2. **Integration Tests** - Współpraca komponentów
3. **API Tests** - Endpointy HTTP
4. **Performance Tests** - Obciążenie systemu

### Uruchomienie:
```bash
python manage.py test
```

## Deployment

### Development:
```bash
python manage.py runserver
```

### Production:
```bash
gunicorn sybase_project.wsgi:application
```

### Docker:
```bash
docker-compose up
```

## Wsparcie

Dokumentacja dodatkowa:
- [README.md](README.md) - Główna dokumentacja
- [QUICKSTART.md](QUICKSTART.md) - Szybki start
- [USAGE.md](USAGE.md) - Przykłady użycia
- [CONTRIBUTING.md](CONTRIBUTING.md) - Współpraca