# TripBudget - System zarządzania budżetem grupowych wycieczek

## Opis projektu

Aplikacja webowa do zarządzania budżetem grupowych wycieczek. Umożliwia tworzenie wycieczek, dodawanie wydatków w różnych walutach, automatyczne rozliczanie między uczestnikami oraz wizualizację statystyk wydatków.

System wspiera wielowalutowość z automatycznym przeliczaniem na PLN według aktualnych kursów NBP, inteligentny algorytm rozliczeń minimalizujący liczbę przelewów oraz interaktywne wykresy przedstawiające strukturę wydatków.

---

## Technologie

### Backend
- **Django 6.0** - framework aplikacji webowych
- **PostgreSQL** - relacyjna baza danych
- **NBP API** - integracja z API Narodowego Banku Polskiego do pobierania kursów walut
- **Python 3.11+** - język programowania
- **Gunicorn** - serwer WSGI do produkcji

### Frontend
- **HTML5** - struktura strony
- **CSS3** - stylizacja
- **JavaScript** - interaktywność
- **Bootstrap 5** - responsywny framework CSS
- **Chart.js** - biblioteka do generowania wykresów
- **Fetch API** - asynchroniczna komunikacja z backendem

### Architektura
- **Multi-Page Application (MPA)** - tradycyjna architektura z serwerowym renderowaniem
- **Wzorzec MVC/MVT** - Django Model-View-Template
- **REST API** - endpointy do operacji AJAX

---

## Wymagania systemowe

- Python 3.11 lub nowszy
- PostgreSQL 12 lub nowszy
- pip (menedżer pakietów Python)

---

## Instalacja i uruchomienie

### 1. Sklonuj repozytorium
```bash
git clone github.com/Wisznior/TripBudget
cd TripBudget
```

### 2. Utwórz środowisko wirtualne
```bash
python -m venv venv
```

### 3. Aktywuj środowisko wirtualne

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### 4. Zainstaluj zależności
```bash
pip install -r requirements.txt
```

### 5. Konfiguracja bazy danych

Utwórz plik .env i wypełnij danymi:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True

DB_NAME=tripbudget_db
DB_USER=your-username
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

### 6. Inicjalizacja bazy danych

Skrypt automatycznie utworzy bazę danych i wykona migracje:

```bash
python setup.py
```

Alternatywnie, ręcznie:
```bash
# Utwórz bazę danych w PostgreSQL
createdb tripbudget_db

# Wykonaj migracje Django
python manage.py migrate
```

### 7. (Opcjonalnie) Utwórz superużytkownika
```bash
python manage.py createsuperuser
```

### 8. Uruchom serwer deweloperski
```bash
python manage.py runserver
```

### 9. Otwórz aplikację w przeglądarce
```
http://127.0.0.1:8000
```

---

## Funkcjonalności

### Uwierzytelnianie i autoryzacja
- Rejestracja nowych użytkowników
- Logowanie z walidacją
- Dwie role użytkowników:
  - **Właściciel wycieczki** - pełne uprawnienia (edycja, usuwanie wydatków, zapraszanie uczestników, zamykanie wycieczki)
  - **Uczestnik** - ograniczone uprawnienia (dodawanie wydatków, przeglądanie szczegółów, opuszczanie wycieczki)

### Zarządzanie wycieczkami
- Tworzenie nowych wycieczek z budżetem i datami
- Zapraszanie uczestników po nazwie użytkownika
- Zamykanie wycieczek (brak możliwości dodawania nowych wydatków)
- Opuszczanie wycieczki przez uczestników (tylko bez wydatków)
- Lista wszystkich wycieczek użytkownika (własne i uczestniczone)

### Zarządzanie wydatkami
- Dodawanie wydatków z następującymi parametrami:
  - Nazwa wydatku
  - Kwota i waluta (PLN, EUR, USD, GBP)
  - Kategoria (Jedzenie, Transport, Nocleg, Rozrywka, Inne)
- Automatyczne przeliczanie walut według kursu NBP
- Usuwanie wydatków przez właściciela wycieczki
- Historia wszystkich wydatków w wycieczce

### System rozliczeń
- Automatyczny algorytm rozliczeń:
  - Obliczanie średniego kosztu na osobę
  - Wyznaczanie bilansu każdego uczestnika
  - Minimalizacja liczby przelewów między uczestnikami
  - Wyświetlanie kto, komu i ile powinien przelać

### Wizualizacja danych
- Wykresy kołowe wydatków według kategorii
- Wykresy słupkowe wydatków według osób
- Karty statystyczne:
  - Całkowity budżet wycieczki
  - Wydana kwota
  - Pozostały budżet
- Dynamiczna aktualizacja wykresów po dodaniu/usunięciu wydatku

### Integracje zewnętrzne
- **NBP API** - automatyczne pobieranie aktualnych kursów walut
- Obsługa błędów API z fallbackiem na kurs 1:1

---

## Struktura projektu

```
TripBudget/
├── backend/                    # Konfiguracja Django
│   ├── __init__.py
│   ├── settings.py             # Ustawienia projektu (baza, middleware, apps)
│   ├── urls.py                 # Routing główny
│   ├── wsgi.py                 # WSGI dla serwera produkcyjnego
│   └── asgi.py                 # ASGI dla aplikacji asynchronicznych
│
├── core/                       # Główna aplikacja
│   ├── migrations/             # Migracje bazy danych
│   ├── templates/              # Szablony HTML
│   │   ├── base.html           # Szablon bazowy (navbar, footer)
│   │   ├── trip_list.html      # Lista wycieczek
│   │   ├── trip_form.html      # Formularz tworzenia wycieczki
│   │   ├── trip_detail.html    # Szczegóły wycieczki z wykresami
│   │   └── registration/       # Strony logowania/rejestracji
│   │       ├── login.html
│   │       └── register.html
│   │
│   ├── static/core/            # Pliki statyczne
│   │   ├── css/
│   │   │   └── style.css       # Własne style CSS
│   │   └── js/
│   │       └── trip_detail.js  # Logika AJAX (dodawanie wydatków, wykres)
│   │
│   ├── __init__.py
│   ├── admin.py                # Panel administracyjny Django
│   ├── apps.py                 # Konfiguracja aplikacji
│   ├── models.py               # Modele (Trip, Expense)
│   ├── views.py                # Widoki (logika biznesowa)
│   ├── forms.py                # Formularze Django
│   ├── urls.py                 # Routing aplikacji
│   └── tests.py                # Testy jednostkowe
│
├── .env                        # Zmienne środowiskowe (NIE commitować!)
├── .env.example                # Szablon zmiennych środowiskowych
├── .gitignore                  # Pliki ignorowane przez Git
├── manage.py                   # Narzędzie CLI Django
├── requirements.txt            # Zależności Python
├── setup.py                    # Skrypt automatycznej inicjalizacji bazy
└── README.md                   # Dokumentacja projektu
```

---

## Modele bazy danych

### Model `Trip` (Wycieczka)
| Pole | Typ | Opis |
|------|-----|------|
| `trip_name` | CharField(200) | Nazwa wycieczki |
| `trip_budget` | DecimalField | Budżet wycieczki w PLN |
| `start_date` | DateField | Data rozpoczęcia |
| `end_date` | DateField | Data zakończenia |
| `trip_owner` | ForeignKey(User) | Właściciel wycieczki |
| `participants` | ManyToManyField(User) | Uczestnicy wycieczki |
| `is_active` | BooleanField | Status aktywności (True/False) |

### Model `Expense` (Wydatek)
| Pole | Typ | Opis |
|------|-----|------|
| `trip` | ForeignKey(Trip) | Powiązana wycieczka |
| `description` | CharField(200) | Opis wydatku |
| `amout` | DecimalField | Kwota w oryginalnej walucie |
| `currency` | CharField(3) | Kod waluty (PLN/EUR/USD/GBP) |
| `amount_pln` | DecimalField | Kwota przeliczona na PLN |
| `category` | CharField(50) | Kategoria (food/transport/accommodation/entertainment/other) |
| `payer` | ForeignKey(User) | Osoba, która zapłaciła |
| `created_at` | DateTimeField | Data dodania |

**Relacje:**
- Trip ↔ User (ForeignKey): właściciel wycieczki
- Trip ↔ User (ManyToMany): uczestnicy wycieczki
- Expense → Trip (ForeignKey): wydatek należy do wycieczki
- Expense → User (ForeignKey): płatnik wydatku

---

## API Endpoints

### Wydatki

#### Dodaj wydatek
```
POST /api/add-expense/<trip_pk>/
Content-Type: application/json

{
  "name": "Pizza Margherita",
  "amount": 45.50,
  "currency": "PLN",
  "category": "food"
}

Odpowiedź (200 OK):
{
  "id": 123,
  "name": "Pizza Margherita",
  "amount": 45.50,
  "currency": "PLN",
  "amount_pln": 45.50,
  "category_display": "Jedzenie",
  "payer": "jan_kowalski",
  "message": "Wydatek dodany!"
}
```

#### Usuń wydatek
```
DELETE /api/delete-expense/<expense_pk>/

Odpowiedź (200 OK):
{
  "message": "Usunięto"
}
```

### Uczestnicy

#### Dodaj uczestnika
```
POST /api/add-participant/<trip_pk>/
Content-Type: application/json

{
  "username": "anna_nowak"
}

Odpowiedź (200 OK):
{
  "message": "Użytkownik dodany",
  "username": "anna_nowak"
}
```

### Wycieczki

#### Opuść wycieczkę
```
POST /trip/<trip_pk>/leave/

Przekierowanie do: /
```

#### Zamknij wycieczkę
```
GET /trip/<trip_pk>/finish/

Przekierowanie do: /trip/<trip_pk>/
```

---

## Algorytm rozliczeń

System wykorzystuje zoptymalizowany algorytm minimalizacji transakcji:

### Krok 1: Obliczenie średniego kosztu
```python
avg_cost = total_spent / number_of_participants
```

### Krok 2: Obliczenie bilansu każdego uczestnika
```python
balance = amount_paid - avg_cost
```

Bilans może być:
- **Dodatni** - uczestnik zapłacił więcej (wierzyciel)
- **Ujemny** - uczestnik zapłacił mniej (dłużnik)
- **Zero** - uczestnik zapłacił dokładnie średnią

### Krok 3: Podział na dłużników i wierzycieli
```python
debtors = [user for user, balance in balances if balance < 0]
creditors = [user for user, balance in balances if balance > 0]
```

### Krok 4: Parowanie dłużników z wierzycielami
Algorytm greedy iteracyjnie paruje dłużników z wierzycielami, minimalizując liczbę transakcji.

---

## Zmienne środowiskowe (.env)

```env
# Django
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL)
DB_NAME=tripbudget_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Opcjonalne
LANGUAGE_CODE=pl-pl
TIME_ZONE=Europe/Warsaw
```

**Uwaga:** Plik `.env` zawiera wrażliwe dane i NIE powinien być commitowany do repozytorium Git!

---

## Licencja

Projekt stworzony na potrzeby akademickie. Wszelkie prawa zastrzeżone.

---

## Autor

**Rafał Wiszniowski**
