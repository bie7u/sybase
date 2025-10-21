# Szybki Start

## 1. Podstawowa instalacja (3 minuty)

```bash
# Sklonuj repozytorium
git clone https://github.com/bie7u/sybase.git
cd sybase

# Utwórz wirtualne środowisko
python -m venv venv
source venv/bin/activate  # Linux/Mac
# lub venv\Scripts\activate  # Windows

# Zainstaluj zależności
pip install -r requirements.txt
```

## 2. Konfiguracja

### Opcja A: Tryb testowy (bez Sybase)

Jeśli nie masz jeszcze Sybase lub chcesz szybko przetestować:

```bash
# Skopiuj przykładową konfigurację
cp .env.example .env

# Edytuj .env i ustaw:
USE_SYBASE=False

# Uruchom migracje
python manage.py migrate

# Uruchom serwer
python manage.py runserver
```

### Opcja B: Połączenie z Sybase

```bash
# Skopiuj przykładową konfigurację
cp .env.example .env

# Edytuj .env i uzupełnij dane Sybase:
USE_SYBASE=True
DB_NAME=twoja_baza
DB_USER=twoj_uzytkownik
DB_PASSWORD=twoje_haslo
DB_HOST=adres_serwera
DB_PORT=5000

# Sprawdź połączenie
python manage.py check_sybase_connection

# Wygeneruj modele z istniejących tabel
python manage.py inspectdb > api/models_generated.py
# Następnie skopiuj potrzebne modele do api/models.py

# Uruchom serwer
python manage.py runserver
```

## 3. Test API

Otwórz przeglądarkę i przejdź do:

```
http://localhost:8000/api/
```

Powinieneś zobaczyć listę dostępnych endpointów.

## 4. Pierwsze zapytania

### Przeglądarka

- Lista klientów: http://localhost:8000/api/customers/
- Lista przykładów: http://localhost:8000/api/examples/

### Curl

```bash
# Lista wszystkich klientów
curl http://localhost:8000/api/customers/

# Wyszukiwanie
curl "http://localhost:8000/api/customers/?search=john"

# Filtrowanie po mieście
curl "http://localhost:8000/api/customers/?city=Warsaw"

# Sortowanie
curl "http://localhost:8000/api/customers/?ordering=-created_date"

# Paginacja
curl "http://localhost:8000/api/customers/?page=2&page_size=20"
```

## 5. Dostosowanie do swoich tabel

1. Wygeneruj modele z bazy:
```bash
python manage.py inspectdb > api/models_generated.py
```

2. Otwórz `api/models_generated.py` i skopiuj interesujące Cię modele do `api/models.py`

3. Upewnij się, że każdy model ma:
```python
class Meta:
    managed = False  # WAŻNE: nie pozwalaj Django zarządzać tabelą
    db_table = 'nazwa_tabeli_w_bazie'
```

4. Utwórz serializery w `api/serializers.py`:
```python
class MojModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MojModel
        fields = '__all__'
```

5. Utwórz ViewSet w `api/views.py`:
```python
class MojModelViewSet(viewsets.ModelViewSet):
    queryset = MojModel.objects.all()
    serializer_class = MojModelSerializer
```

6. Zarejestruj w `api/urls.py`:
```python
router.register(r'mojmodel', MojModelViewSet, basename='mojmodel')
```

## 6. Gotowe!

Twoje API jest gotowe do użycia! 

### Dalsze kroki:

- Przeczytaj [USAGE.md](USAGE.md) dla szczegółowych przykładów
- Sprawdź [README.md](README.md) dla pełnej dokumentacji
- Dodaj własne filtry w `api/filters.py`
- Dostosuj serializery według potrzeb
- Dodaj własne custom endpoints w ViewSet

## Troubleshooting

### Problem: Błąd połączenia z Sybase

```bash
# Sprawdź połączenie
python manage.py check_sybase_connection

# Sprawdź czy FreeTDS jest zainstalowany
isql -v

# Sprawdź czy zmienne środowiskowe są poprawne
env | grep DB_
```

### Problem: ModuleNotFoundError

```bash
# Zainstaluj brakujące zależności
pip install -r requirements.txt
```

### Problem: pyodbc nie działa

```bash
# Linux
sudo apt-get install unixodbc unixodbc-dev

# Mac
brew install unixodbc

# Następnie przeinstaluj pyodbc
pip install --no-cache-dir pyodbc
```

## Wsparcie

Problemy? Otwórz issue na GitHub: https://github.com/bie7u/sybase/issues
