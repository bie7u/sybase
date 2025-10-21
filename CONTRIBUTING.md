# Przewodnik dla kontrybutorów

Dziękujemy za zainteresowanie rozwojem projektu Django Sybase!

## Jak pomóc?

### Zgłaszanie błędów

1. Sprawdź czy błąd nie został już zgłoszony w Issues
2. Użyj szablonu zgłoszenia błędu
3. Dołącz:
   - Opis problemu
   - Kroki do odtworzenia
   - Oczekiwane zachowanie
   - Aktualne zachowanie
   - Środowisko (wersja Python, Django, system operacyjny)

### Propozycje nowych funkcji

1. Sprawdź czy funkcja nie została już zaproponowana
2. Opisz use case
3. Wyjaśnij dlaczego ta funkcja byłaby przydatna

### Pull Requesty

1. Forkuj repozytorium
2. Utwórz branch dla swojej funkcji (`git checkout -b feature/AmazingFeature`)
3. Commituj zmiany (`git commit -m 'Add some AmazingFeature'`)
4. Push do brancha (`git push origin feature/AmazingFeature`)
5. Otwórz Pull Request

### Standardy kodu

- Używaj PEP 8 dla kodu Python
- Dodawaj docstringi do funkcji i klas
- Pisz testy dla nowych funkcji
- Aktualizuj dokumentację

### Testowanie

Przed wysłaniem PR:

```bash
# Zainstaluj zależności deweloperskie
pip install -r requirements.txt

# Uruchom testy
python manage.py test

# Sprawdź formatowanie
flake8 .
```

## Pytania?

Jeśli masz pytania, otwórz issue lub skontaktuj się z maintainerem.

Dziękujemy za wkład!
