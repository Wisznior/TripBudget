from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Trip(models.Model):
    #nazwa wycieczki
    trip_name = models.CharField(max_length = 100, verbose_name = "Twoja nazwa wycieczki")

    #budżet wycieczki
    trip_budget = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name = "Twój budżet")

    start_date = models.DateField(verbose_name = "Data początku wycieczki")
    end_date = models.DateField(verbose_name = "Data zakończenia wycieczki")

    trip_owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'trips')

    participants = models.ManyToManyField(User, related_name = 'participated_trips', blank = True)

    is_active = models.BooleanField(default = True, verbose_name = "Czy aktywna?")

    def __str__(self):
        return f"{self.trip_name} ({self.start_date})"

class Expense(models.Model):
    CATEGORIES = [
        ('transport', 'Transport'),
        ('food', 'Jedzenie'),
        ('accomodation', 'Zakwaterowanie'),
        ('entertainment', 'Rozrywka'),
        ('other', 'Inne'),
    ]

    trip = models.ForeignKey(Trip, on_delete = models.CASCADE, related_name = "wydatki")

    description = models.CharField(max_length = 100, verbose_name = "Opis wydatku")
    
    CURRENCY_CHOICES = [
        ('PLN', 'Polski Złoty'),
        ('EUR', 'Euro'),
        ('USD', 'Dolar Amerykański'),
        ('GBP', 'Funt Brytyjski'),
    ]

    currency = models.CharField(max_length = 3, choices = CURRENCY_CHOICES, default = 'PLN', verbose_name = "Waluta")

    amount_pln = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name = "Kwota wydatku w PLN", default = 0)

    amout = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name = "Kwota wydatku")

    category = models.CharField(max_length = 20, choices = CATEGORIES, default = 'other', verbose_name = "Kategoria wydatku")

    payer = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, verbose_name = "Kto płacił")
    
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.description} - {self.amout} PLN"