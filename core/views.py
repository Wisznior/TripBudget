import json
import requests
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.decorators.http import require_POST, require_http_methods
from django.http import JsonResponse
from django.db.models import Sum, Q
from .models import Trip, Expense
from .forms import TripForm
from django.contrib.auth.models import User

#NBP - funkcja pomocnicza
def get_nbp_rate(currency_code):
    """Pobiera kurs waluty z NBP. Jeśli błąd lub PLN, zwraca 1.0"""
    if currency_code == 'PLN':
        return Decimal(1.0)
    
    try:
        url = f"http://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/?format=json"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            rate = data['rates'][0]['mid']
            return Decimal(rate)
    except Exception as e:
        print(f"Błąd NBP: {e}")
    
    return Decimal(1.0)

#rejestracja
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('trip_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

#lista wycieczek
@login_required
def trip_list(request):
    trips = Trip.objects.filter(
        Q(trip_owner=request.user) | Q(participants=request.user)
    ).distinct()
    return render(request, 'trip_list.html', {'trips': trips})

#tworzenie wycieczki
@login_required
def trip_create(request):
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.trip_owner = request.user
            trip.save()
            return redirect('trip_list')
    else:
        form = TripForm()
    return render(request, 'trip_form.html', {'form': form})

#zamknięcie wycieczki
@login_required
def finish_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.user == trip.trip_owner:
        trip.is_active = False
        trip.save()
    return redirect('trip_detail', pk=pk)

#szczegóły wycieczki
@login_required
def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    
    is_participant = trip.participants.filter(id=request.user.id).exists()
    is_owner = (trip.trip_owner == request.user)
    if not is_owner and not is_participant:
        return redirect('trip_list')
    
    total_spent = trip.wydatki.aggregate(total=Sum('amount_pln'))['total'] or 0
    remaining_budget = trip.trip_budget - total_spent

    stats_category = trip.wydatki.values('category').annotate(total=Sum('amount_pln'))
    labels_cat = [item['category'] for item in stats_category]
    data_cat = [float(item['total']) for item in stats_category]

    stats_payer = trip.wydatki.values('payer__username').annotate(total=Sum('amount_pln'))
    labels_payer = [item['payer__username'] if item['payer__username'] else 'Nieznany' for item in stats_payer]
    data_payer = [float(item['total']) for item in stats_payer]

    settlements = [] 
    avg_cost = 0
    
    if total_spent > 0:
        participants = list(trip.participants.all())
        participants.append(trip.trip_owner)
        participants = list(set(participants))
        count = len(participants)
        
        if count > 0:
            avg_cost = round(total_spent / count, 2)
            
            balances = {}
            for p in participants:
                paid = trip.wydatki.filter(payer=p).aggregate(s=Sum('amount_pln'))['s'] or 0
                balances[p.username] = float(paid) - float(avg_cost)

            debtors = []
            creditors = []
            for user, amount in balances.items():
                if amount < -0.01: debtors.append({'user': user, 'amount': amount})
                elif amount > 0.01: creditors.append({'user': user, 'amount': amount})
                
            debtor_idx = 0
            creditor_idx = 0
            
            while debtor_idx < len(debtors) and creditor_idx < len(creditors):
                debtor = debtors[debtor_idx]
                creditor = creditors[creditor_idx]
                
                amount = min(abs(debtor['amount']), creditor['amount'])
                
                if amount > 0:
                    settlements.append({
                        'from': debtor['user'],
                        'to': creditor['user'],
                        'amount': round(amount, 2)
                    })
                
                debtor['amount'] += amount
                creditor['amount'] -= amount
                
                if abs(debtor['amount']) < 0.01: debtor_idx += 1
                if creditor['amount'] < 0.01: creditor_idx += 1

    user_expenses_count = trip.wydatki.filter(payer=request.user).count()

    context = {
        'trip': trip,
        'is_owner': is_owner,
        'total_spent': total_spent,
        'remaining_budget': remaining_budget,
        'labels_cat': json.dumps(labels_cat),
        'data_cat': json.dumps(data_cat),
        'labels_payer': json.dumps(labels_payer),
        'data_payer': json.dumps(data_payer),
        'settlements': settlements,
        'avg_cost': avg_cost,
        'user_expenses_count': user_expenses_count,
    }
    return render(request, 'trip_detail.html', context)

#dodawanie wydatku
@login_required
@require_POST
def add_expense_api(request, trip_pk):
    trip = get_object_or_404(Trip, pk=trip_pk)
    data = json.loads(request.body)
    
    currency = data.get('currency', 'PLN')
    try:
        original_amount = Decimal(str(data.get('amount')))
    except:
        return JsonResponse({'error': 'Błędna kwota'}, status=400)
    
    rate = get_nbp_rate(currency)
    amount_in_pln = original_amount * rate
    
    expense = Expense.objects.create(
        trip=trip,
        description=data.get('name'),
        amout=original_amount,
        currency=currency,
        amount_pln=amount_in_pln,
        category=data.get('category'),
        payer=request.user
    )
    
    return JsonResponse({
        'id': expense.id,
        'name': expense.description,
        'amount': expense.amout,
        'currency': expense.currency,
        'amount_pln': round(expense.amount_pln, 2),
        'category_display': expense.get_category_display(),
        'payer': expense.payer.username,
        'message': 'Wydatek dodany!'
    })

#usuwanie wydatku
@login_required
@require_http_methods(["DELETE"])
def delete_expense_api(request, expense_pk):
    expense = get_object_or_404(Expense, pk=expense_pk)
    if request.user != expense.trip.trip_owner:
        return JsonResponse({'error': 'Brak uprawnień'}, status=403)
    expense.delete()
    return JsonResponse({'message': 'Usunięto'})

#dodawanie uczestniak
@login_required
@require_POST
def add_participant_api(request, trip_pk):
    trip = get_object_or_404(Trip, pk=trip_pk)

    if request.user != trip.trip_owner:
        return JsonResponse({'error': 'Brak uprawnień'}, status=403)
    
    data = json.loads(request.body)
    username = data.get('username')

    try:
        user_to_add = User.objects.get(username=username)
        if user_to_add == trip.trip_owner:
            return JsonResponse({'error': 'To właściciel wycieczki'}, status=400)
        
        trip.participants.add(user_to_add)
        return JsonResponse({'message': 'Użytkownik dodany', 'username': user_to_add.username})
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'Nie znaleziono użytkownika'}, status=404)

#opuszczenie wycieczki
@login_required
def leave_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk)

    is_participant = trip.participants.filter(id = request.user.id).exists()
    is_owner = (trip.trip_owner == request.user)
    
    if is_owner:
        return redirect('trip_detail', pk=pk)
    
    if not is_participant:
        return redirect('trip_list')
    
    user_expenses = trip.wydatki.filter(payer=request.user)
    
    if user_expenses.exists():
        return redirect('trip_detail', pk=pk)
    
    trip.participants.remove(request.user)
    
    return redirect('trip_list')