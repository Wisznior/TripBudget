document.addEventListener('DOMContentLoaded', function() {
    console.log("TripBudget: JS załadowany.");

    const configDiv = document.getElementById('trip-config');
    
    if (!configDiv) {
        return;
    }

    const addUrl = configDiv.dataset.addUrl;
    
    const getCsrfToken = () => {
        const input = document.querySelector('[name=csrfmiddlewaretoken]');
        return input ? input.value : '';
    };

    const ctxCat = document.getElementById('categoryChart');
    const ctxPayer = document.getElementById('payerChart');

    if (ctxCat && ctxPayer) {
        try {
            const getJsonData = (id) => {
                const el = document.getElementById(id);
                if (!el) {
                    console.warn(`Brak elementu danych: ${id}`);
                    return [];
                }

                let parsed = JSON.parse(el.textContent);

                if (typeof parsed === 'string') {
                    parsed = JSON.parse(parsed);
                }
                
                return parsed;
            };

            const labelsCat = getJsonData('labels-cat-data');
            const dataCat = getJsonData('data-cat-data');
            const labelsPayer = getJsonData('labels-payer-data');
            const dataPayer = getJsonData('data-payer-data');

            const colors = [
                '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40',
                '#E91E63', '#8BC34A', '#795548', '#607D8B' 
            ];

            //wykres kategori
            if (Array.isArray(labelsCat) && labelsCat.length > 0) {
                new Chart(ctxCat, {
                    type: 'doughnut',
                    data: {
                        labels: labelsCat,
                        datasets: [{
                            data: dataCat,
                            backgroundColor: colors,
                            borderWidth: 2,
                            borderColor: '#ffffff'
                        }]
                    },
                    options: { maintainAspectRatio: false }
                });
            }

            //wykres uczestnikow
            if (Array.isArray(labelsPayer) && labelsPayer.length > 0) {
                new Chart(ctxPayer, {
                    type: 'bar',
                    data: {
                        labels: labelsPayer,
                        datasets: [{
                            label: 'Wydano (PLN)',
                            data: dataPayer,
                            backgroundColor: colors,
                            borderRadius: 6,
                            borderWidth: 1
                        }]
                    },
                    options: { 
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false }
                        },
                        scales: { 
                            y: { beginAtZero: true, grid: { display: false } }, 
                            x: { grid: { display: false } } 
                        } 
                    }
                });
            }
            console.log("Wykresy wygenerowane pomyślnie.");

        } catch (error) {
            console.error("Błąd generowania wykresów:", error);
        }
    }

    //dodawanie wydatku - fetch
    const addForm = document.getElementById('add-expense-form');
    if (addForm) {
        addForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = {
                name: this.name.value,
                amount: this.amount.value,
                category: this.category.value,
                currency: this.currency.value
            };

            fetch(addUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', 
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify(formData)
            })
            .then(res => { 
                if(!res.ok) throw new Error("Błąd sieci lub serwera"); 
                return res.json(); 
            })
            .then(data => {
                window.location.reload();
            })
            .catch(err => {
                console.error("Błąd dodawania:", err);
                alert("Nie udało się dodać wydatku. Sprawdź konsolę.");
            });
        });
    }

    //usuwanie wydatku
    const expensesList = document.getElementById('expenses-list');
    if (expensesList) {
        expensesList.addEventListener('click', function(e) {
            const btn = e.target.closest('.delete-btn');
            if(btn) {
                if(!confirm('Usunąć ten wydatek?')) return;
                const id = btn.getAttribute('data-id');
                
                fetch(`/api/delete-expense/${id}/`, {
                    method: 'DELETE',
                    headers: {'X-CSRFToken': getCsrfToken()}
                }).then(res => { if(res.ok) window.location.reload(); });
            }
        });
    }
    
    //dodawanie uczestnika
    const partForm = document.getElementById('add-participant-form');
    if (partForm) {
        partForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const url = configDiv.dataset.addParticipantUrl;

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', 
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({ username: this.username.value })
            })
            .then(res => res.json())
            .then(data => {
                if(data.message) window.location.reload();
                else document.getElementById('participant-msg').textContent = data.error;
            });
        });
    }
});