# Przewodnik użytkowania Django Sybase API

## Szybki start

### 1. Instalacja i konfiguracja

```bash
# Klonowanie repozytorium
git clone https://github.com/bie7u/sybase.git
cd sybase

# Utworzenie środowiska wirtualnego
python -m venv venv
source venv/bin/activate  # Linux/Mac

# Instalacja zależności
pip install -r requirements.txt

# Konfiguracja
cp .env.example .env
# Edytuj .env i uzupełnij danymi swojej bazy Sybase

# Uruchomienie serwera
python manage.py runserver
```

### 2. Generowanie modeli z istniejących tabel

Django może automatycznie wygenerować modele na podstawie istniejących tabel w bazie:

```bash
python manage.py inspectdb > api/models_generated.py
```

Następnie:
1. Otwórz `api/models_generated.py`
2. Skopiuj potrzebne modele do `api/models.py`
3. Dostosuj według potrzeb (dodaj `managed = False` w Meta)
4. Usuń plik `models_generated.py`

## Szczegółowe przykłady użycia API

### Podstawowe operacje CRUD

#### 1. Pobranie listy rekordów (GET)

```bash
curl http://localhost:8000/api/customers/
```

Odpowiedź:
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/customers/?page=2",
  "previous": null,
  "results": [
    {
      "customer_id": 1,
      "first_name": "Jan",
      "last_name": "Kowalski",
      "email": "jan.kowalski@example.com",
      "city": "Warsaw",
      "country": "Poland"
    },
    ...
  ]
}
```

#### 2. Pobranie szczegółów rekordu (GET)

```bash
curl http://localhost:8000/api/customers/1/
```

Odpowiedź:
```json
{
  "customer_id": 1,
  "first_name": "Jan",
  "last_name": "Kowalski",
  "full_name": "Jan Kowalski",
  "email": "jan.kowalski@example.com",
  "phone": "+48123456789",
  "address": "ul. Przykładowa 1",
  "city": "Warsaw",
  "country": "Poland",
  "created_date": "2024-01-15T10:30:00Z"
}
```

#### 3. Utworzenie nowego rekordu (POST)

```bash
curl -X POST http://localhost:8000/api/customers/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Anna",
    "last_name": "Nowak",
    "email": "anna.nowak@example.com",
    "phone": "+48987654321",
    "city": "Krakow",
    "country": "Poland"
  }'
```

#### 4. Aktualizacja rekordu (PUT)

```bash
curl -X PUT http://localhost:8000/api/customers/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jan",
    "last_name": "Kowalski",
    "email": "jan.nowy@example.com",
    "phone": "+48111222333",
    "city": "Gdansk",
    "country": "Poland"
  }'
```

#### 5. Częściowa aktualizacja (PATCH)

```bash
curl -X PATCH http://localhost:8000/api/customers/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jan.updated@example.com"
  }'
```

#### 6. Usunięcie rekordu (DELETE)

```bash
curl -X DELETE http://localhost:8000/api/customers/1/
```

### Zaawansowane filtrowanie

#### Filtrowanie po pojedynczym polu

```bash
# Klienci z Warszawy
curl "http://localhost:8000/api/customers/?city=Warsaw"

# Klienci z Polski
curl "http://localhost:8000/api/customers/?country=Poland"

# Filtrowanie po nazwisku (zawiera)
curl "http://localhost:8000/api/customers/?last_name=Kowalski"
```

#### Filtrowanie po wielu polach

```bash
curl "http://localhost:8000/api/customers/?city=Warsaw&country=Poland"
```

#### Filtrowanie po datach

```bash
# Klienci utworzeni po określonej dacie
curl "http://localhost:8000/api/customers/?created_after=2024-01-01"

# Klienci utworzeni przed określoną datą
curl "http://localhost:8000/api/customers/?created_before=2024-12-31"

# Klienci z zakresu dat
curl "http://localhost:8000/api/customers/?created_after=2024-01-01&created_before=2024-06-30"
```

### Wyszukiwanie

Wyszukiwanie działa na wielu polach jednocześnie:

```bash
# Wyszukiwanie "john" w imię, nazwisko, email, miasto, kraj
curl "http://localhost:8000/api/customers/?search=john"
```

### Sortowanie

```bash
# Sortowanie rosnąco po nazwisku
curl "http://localhost:8000/api/customers/?ordering=last_name"

# Sortowanie malejąco po dacie utworzenia
curl "http://localhost:8000/api/customers/?ordering=-created_date"

# Sortowanie po wielu polach
curl "http://localhost:8000/api/customers/?ordering=country,city,last_name"
```

### Paginacja

```bash
# Pierwsza strona (domyślnie 10 rekordów)
curl "http://localhost:8000/api/customers/"

# Druga strona
curl "http://localhost:8000/api/customers/?page=2"

# Zmiana rozmiaru strony na 25 rekordów
curl "http://localhost:8000/api/customers/?page_size=25"

# Trzecia strona z 50 rekordami na stronę
curl "http://localhost:8000/api/customers/?page=3&page_size=50"
```

### Łączenie wszystkich parametrów

```bash
curl "http://localhost:8000/api/customers/?city=Warsaw&country=Poland&search=jan&ordering=-created_date&page=1&page_size=20"
```

### Custom endpoints

#### Grupowanie klientów po kraju

```bash
curl "http://localhost:8000/api/customers/by_country/"
```

Odpowiedź:
```json
[
  {
    "country": "Poland",
    "count": 150
  },
  {
    "country": "Germany",
    "count": 75
  },
  ...
]
```

#### Aktywne przykłady

```bash
curl "http://localhost:8000/api/examples/active/"
```

## Integracja z Python

### Używanie requests

```python
import requests

# Pobranie listy klientów
response = requests.get('http://localhost:8000/api/customers/')
customers = response.json()

print(f"Liczba klientów: {customers['count']}")
for customer in customers['results']:
    print(f"{customer['first_name']} {customer['last_name']}")

# Utworzenie nowego klienta
new_customer = {
    'first_name': 'Piotr',
    'last_name': 'Wiśniewski',
    'email': 'piotr.wisniewski@example.com',
    'city': 'Wroclaw',
    'country': 'Poland'
}
response = requests.post(
    'http://localhost:8000/api/customers/',
    json=new_customer
)
created_customer = response.json()
print(f"Utworzono klienta o ID: {created_customer['customer_id']}")

# Filtrowanie i wyszukiwanie
params = {
    'city': 'Warsaw',
    'ordering': '-created_date',
    'page_size': 20
}
response = requests.get('http://localhost:8000/api/customers/', params=params)
filtered_customers = response.json()
```

## Dodawanie nowych endpointów

### 1. Utwórz model w `api/models.py`

```python
class Product(models.Model):
    product_id = models.AutoField(primary_key=True, db_column='product_id')
    name = models.CharField(max_length=200, db_column='name')
    price = models.DecimalField(max_digits=10, decimal_places=2, db_column='price')
    stock = models.IntegerField(db_column='stock')
    
    class Meta:
        managed = False
        db_table = 'products'
        ordering = ['name']
```

### 2. Utwórz serializer w `api/serializers.py`

```python
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'price', 'stock']
        read_only_fields = ['product_id']
```

### 3. Utwórz filtr w `api/filters.py`

```python
class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock']
```

### 4. Utwórz ViewSet w `api/views.py`

```python
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name']
    ordering_fields = ['product_id', 'name', 'price', 'stock']
    ordering = ['name']
```

### 5. Zarejestruj w routerze w `api/urls.py`

```python
from .views import ProductViewSet

router.register(r'products', ProductViewSet, basename='product')
```

Teraz możesz używać:
- `GET /api/products/`
- `POST /api/products/`
- `GET /api/products/{id}/`
- `PUT /api/products/{id}/`
- `PATCH /api/products/{id}/`
- `DELETE /api/products/{id}/`

## Konfiguracja dla różnych środowisk

### Rozwój (Development)

```
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Testowanie (Testing)

```
DEBUG=True
ALLOWED_HOSTS=test.example.com
```

### Produkcja (Production)

```
DEBUG=False
ALLOWED_HOSTS=api.example.com,www.example.com
SECRET_KEY=bardzo-długi-i-skomplikowany-klucz-tajny
```

## Bezpieczeństwo

### 1. Zawsze używaj HTTPS w produkcji

### 2. Użyj zmiennych środowiskowych dla wrażliwych danych

### 3. Ogranicz ALLOWED_HOSTS

### 4. Użyj silnego SECRET_KEY

```python
import secrets
print(secrets.token_urlsafe(50))
```

### 5. Konfiguruj CORS jeśli potrzebne

```bash
pip install django-cors-headers
```

## Monitoring i logi

Django automatycznie loguje błędy. Sprawdź:

```bash
tail -f /path/to/your/logs/django.log
```

## Wsparcie

Jeśli potrzebujesz pomocy:
1. Sprawdź dokumentację Django: https://docs.djangoproject.com/
2. Sprawdź dokumentację DRF: https://www.django-rest-framework.org/
3. Utwórz issue w repozytorium GitHub