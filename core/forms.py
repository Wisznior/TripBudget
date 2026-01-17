from django import forms
from .models import Trip

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['trip_name', 'trip_budget', 'start_date', 'end_date']
        widgets = {
            'trip_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'np. Eurotrip'
            }),
            'trip_budget': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholrder': 0.00
            }),
            'start_date': forms.DateInput(attrs = {
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs = {
                'class': 'form-control',
                'type': 'date'
            }),
        }