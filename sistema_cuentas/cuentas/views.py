from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from cuentas.models import Income, Expense
from .forms import IncomeForm, ExpenseForm

# Create your views here.
def index(request):
    context = {}
    return render(request, "cuentas/index.html", context)
def incomes(request):
    incomes = Income.objects.all()
    form = IncomeForm()
    context = {"incomes": incomes, 'form': form}
    return render(request, "cuentas/incomes.html", context)
# Detail View
def income_detail(request, pk):
    income = get_object_or_404(Income, pk=pk)
    return render(request, 'cuentas/income_detail.html', {'income': income})

# Create View
def income_create(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('cuentas:incomes'))
    else:
        form = IncomeForm()
    return render(request, 'cuentas/income_form.html', {'form': form})

# Update View
def income_update(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect(reverse('cuentas:incomes'))
    else:
        form = IncomeForm(instance=income)
    return render(request, 'cuentas/income_form.html', {'form': form})

# Delete View
def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == 'POST':
        income.delete()
        return redirect(reverse('cuentas:incomes'))
    return render(request, 'cuentas/income_confirm_delete.html', {'income': income})

def expenses(request):
    expenses = Expense.objects.all()
    form = ExpenseForm()
    context = {"expenses": expenses, 'form': form}
    return render(request, "cuentas/expenses.html", context)

# Create View
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('cuentas:expenses'))
    else:
        form = ExpenseForm()
    return render(request, 'cuentas/expense_form.html', {'form': form})

# Update View
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect(reverse('cuentas:expenses'))
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'cuentas/expense_form.html', {'form': form})

# Delete View
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect(reverse('cuentas:expenses'))
    return render(request, 'cuentas/expense_confirm_delete.html', {'expense': expense})