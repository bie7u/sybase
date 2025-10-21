# Django Sybase Application

Aplikacja Django łącząca się z bazą danych Sybase poprzez SQLAlchemy, wykorzystująca Django ORM z widokami DRF obsługującymi paginację i filtrowanie.

## Funkcjonalności

- ✅ Połączenie z bazą danych Sybase
- ✅ Integracja SQLAlchemy jako backend bazy danych
- ✅ Django ORM do operacji na bazie danych
- ✅ Django REST Framework (DRF) dla API
- ✅ Paginacja wyników
- ✅ Filtrowanie danych (django-filters)
- ✅ Wyszukiwanie i sortowanie
- ✅ Modele mapujące istniejące tabele w bazie

## Wymagania

- Python 3.8+
- Baza danych Sybase
- FreeTDS (dla połączenia ODBC)
- Sterownik ODBC

## Instalacja

### 1. Sklonuj repozytorium

```bash
git clone https://github.com/bie7u/sybase.git
cd sybase
```

### 2. Utwórz wirtualne środowisko

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# lub
venv\Scripts\activate  # Windows
```

### 3. Zainstaluj zależności

```bash
pip install -r requirements.txt
```

### 4. Konfiguracja

Skopiuj plik `.env.example` do `.env` i uzupełnij danymi swojej bazy:

```bash
cp .env.example .env
```

Edytuj plik `.env`:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_sybase_host
DB_PORT=5000
```

### 5. Generowanie modeli z istniejących tabel

Jeśli masz już tabele w bazie Sybase, możesz wygenerować modele Django:

```bash
python manage.py inspectdb > api/models_generated.py
```

Następnie dostosuj wygenerowane modele według potrzeb i przenieś je do `api/models.py`.

### 6. Uruchomienie serwera

```bash
python manage.py runserver
```

Aplikacja będzie dostępna pod adresem: `http://localhost:8000`

## Struktura projektu

```
sybase/
├── api/                      # Aplikacja API
│   ├── models.py            # Modele Django mapujące tabele Sybase
│   ├── serializers.py       # Serializery DRF
│   ├── views.py             # ViewSets DRF z paginacją i filtrowaniem
│   ├── filters.py           # Filtry dla django-filters
│   ├── urls.py              # Routing URL dla API
│   └── admin.py             # Konfiguracja Django Admin
├── sybase_project/          # Główny projekt Django
│   ├── settings.py          # Ustawienia projektu
│   ├── urls.py              # Główny routing URL
│   └── wsgi.py              # WSGI application
├── sqlalchemy_sybase/       # Backend bazy danych Sybase
│   └── base.py              # Implementacja backendu SQLAlchemy
├── manage.py                # Django management script
├── requirements.txt         # Zależności Python
├── .env.example             # Przykładowa konfiguracja
└── README.md                # Ta dokumentacja
```

## Użycie API

### Endpoints

API dostępne jest pod prefixem `/api/`:

#### Przykładowe tabele (ExampleTable)

- `GET /api/examples/` - Lista wszystkich rekordów (z paginacją)
- `POST /api/examples/` - Utworzenie nowego rekordu
- `GET /api/examples/{id}/` - Pobranie szczegółów rekordu
- `PUT /api/examples/{id}/` - Aktualizacja rekordu
- `PATCH /api/examples/{id}/` - Częściowa aktualizacja
- `DELETE /api/examples/{id}/` - Usunięcie rekordu
- `GET /api/examples/active/` - Lista aktywnych rekordów

#### Klienci (Customers)

- `GET /api/customers/` - Lista wszystkich klientów (z paginacją)
- `POST /api/customers/` - Dodanie nowego klienta
- `GET /api/customers/{id}/` - Szczegóły klienta
- `PUT /api/customers/{id}/` - Aktualizacja klienta
- `PATCH /api/customers/{id}/` - Częściowa aktualizacja
- `DELETE /api/customers/{id}/` - Usunięcie klienta
- `GET /api/customers/by_country/` - Grupowanie według kraju

### Paginacja

Wszystkie listy są automatycznie paginowane (domyślnie 10 rekordów na stronę):

```bash
# Pierwsza strona
GET /api/customers/

# Druga strona
GET /api/customers/?page=2

# Zmiana rozmiaru strony
GET /api/customers/?page_size=20
```

### Filtrowanie

Przykłady filtrowania:

```bash
# Filtrowanie klientów po mieście
GET /api/customers/?city=Warsaw

# Filtrowanie po nazwisku (zawiera)
GET /api/customers/?last_name=Smith

# Wiele filtrów jednocześnie
GET /api/customers/?city=Warsaw&country=Poland

# Filtrowanie po dacie (utworzone po określonej dacie)
GET /api/customers/?created_after=2024-01-01
```

### Wyszukiwanie

Wyszukiwanie w wielu polach naraz:

```bash
# Wyszukiwanie w imię, nazwisko, email, miasto, kraj
GET /api/customers/?search=john
```

### Sortowanie

Sortowanie wyników:

```bash
# Sortowanie rosnąco po nazwisku
GET /api/customers/?ordering=last_name

# Sortowanie malejąco (prefix -)
GET /api/customers/?ordering=-created_date

# Sortowanie po wielu polach
GET /api/customers/?ordering=country,last_name
```

### Łączenie parametrów

Wszystkie parametry można łączyć:

```bash
GET /api/customers/?city=Warsaw&ordering=-created_date&page=2&page_size=20&search=john
```

## Konfiguracja dla produkcji

### 1. Bezpieczeństwo

W produkcji **koniecznie** zmień:

```python
# .env
SECRET_KEY=zmień-na-długi-losowy-ciąg-znaków
DEBUG=False
ALLOWED_HOSTS=twoja-domena.com,www.twoja-domena.com
```

### 2. Pliki statyczne

```bash
python manage.py collectstatic
```

### 3. WSGI Server

Użyj serwera WSGI jak Gunicorn:

```bash
pip install gunicorn
gunicorn sybase_project.wsgi:application
```

## Dodawanie własnych tabel

1. Dodaj model w `api/models.py`:

```python
class YourTable(models.Model):
    # Twoje pola...
    
    class Meta:
        managed = False  # Nie pozwalaj Django zarządzać tabelą
        db_table = 'your_existing_table_name'
```

2. Utwórz serializer w `api/serializers.py`

3. Dodaj filtr w `api/filters.py`

4. Utwórz ViewSet w `api/views.py`

5. Zarejestruj w routerze w `api/urls.py`

## Testowanie

Możesz przetestować API używając:

- Przeglądarki: `http://localhost:8000/api/`
- curl:
  ```bash
  curl http://localhost:8000/api/customers/
  ```
- Postman lub podobne narzędzia

## Rozwiązywanie problemów

### Błąd połączenia z bazą danych

Sprawdź:
1. Czy Sybase jest uruchomiony
2. Czy dane w `.env` są poprawne
3. Czy FreeTDS jest zainstalowany i skonfigurowany
4. Czy firewall nie blokuje połączenia

### Błąd importu SQLAlchemy

```bash
pip install sqlalchemy pyodbc
```

## Licencja

MIT

## Autor

bie7u

## Wsparcie

W razie problemów, utwórz issue w repozytorium GitHub.