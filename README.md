1. Opis projektu:
Aplikacja webowa do zarządzania budżetem grupowych wycieczek. Umożliwia tworzenie wycieczek, dodawanie wydatków w różnych walutach, automatyczne rozliczanie między uczestnikami, wizualizację statystyk.

2. Technologie:
Backend:
- Django ( python )
- PostgreSQL ( baza danych )
- NBP API ( kursy walut )

Frontend:
- HTML5 + CSS3
- JavaScript ( Fetch API )
- Bootstrap 5 ( framework CSS )
- Chart.js - wykresy

Architektura:
- Multi-Page Application
- Wzorzec MVC

3. Uruchomienie
a. venv
python -m venv venv

b. aktywacja venv
( Windows ) venv\Scripts\activate
( Linux ) source venv/bin/activate

c. requitements.txt
pip install -r requirements.txt

d. baza
wpisać dane do logowania do bazy postgresql do .env
python setup.py

e. uruchomienie serwera
python manage.py runserver

f. adres strony
http://127.0.0.1:8000

4. Funkcjonalności:
- Uwierzytelnianie i autoryzacja ( dwie role - właściciel wycieczki, uczestnik )

- Zarządzanie wycieczkami ( tworzenie wycieczki, zapraszanie uczestnikow, zakończenie wycieczki )

- Wydatki ( Dodawanie wydatków - 4 możliwe waluty, automatyczne przeliczanie kursów, wybieranie kategorii wydatku )

- Rozliczenia ( algorytm automatycznego rozliczenia, minimalizacja transakcji, kto komu ile jest winny )

- Statystyki ( wykres wydatkówwedług kategorii, wykres wydatków według osoby )

5. Struktura projektu:

TripBudget/
├── backend/              # Konfiguracja Django
│   ├── settings.py       # Ustawienia projektu
│   ├── urls.py           # Routing
│   └── wsgi.py
├── core/                 # Główna aplikacja
│   ├── models.py         # Modele (Trip, Expense)
│   ├── views.py          # Logika biznesowa
│   ├── forms.py          # Formularze
│   ├── templates/        # Szablony HTML
│   │   ├── base.html
│   │   ├── trip_list.html
│   │   ├── trip_detail.html
│   │   └── registration/
│   └── static/core/      # CSS, JS
│       ├── css/style.css
│       └── js/trip_detail.js
├── manage.py
└── requirements.txt

6. Baza danych
Trip:
- trip_name
- trip_budget
- start_date
- end_date
- trip_owner
- participants
- is_active

Expense:
- trip
- description
- amout
- currency
- amout_pln
- category
- payer

7. Endpoints
- /api/add-expense/<trip_pk>/ - ( POST - dodanie wydatku )

- /api/delete-expense/<expense_pk>/ - ( DELETE - usuwanie wydatku )

- /api/add-participant/<trip_pk>/ - ( POST - dodanie uczestnika )

Autor: Rafał Wiszniowski