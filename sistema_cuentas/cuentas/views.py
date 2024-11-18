from django.shortcuts import render
from cuentas.models import Income, Expense
# Create your views here.
def index(request):
    context = {}
    return render(request, "cuentas/index.html", context)
def incomes(request):
    incomes = Income.objects.all()
    context = {"incomes": incomes}
    return render(request, "cuentas/incomes.html", context)