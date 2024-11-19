from django.urls import path

from . import views

app_name = "cuentas"
urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    path("entradas", views.incomes, name="incomes"),
    path("entradas/<int:pk>/", views.income_detail, name="income_detail"),
    path("entradas/crear/", views.income_create, name="income_create"),
    path("entradas/<int:pk>/editar/", views.income_update, name="income_update"),
    path("entradas/<int:pk>/eliminar/", views.income_delete, name="income_delete"),
    path("gastos", views.expenses, name="expenses"),
    path("gastos/<int:pk>/", views.income_detail, name="expense_detail"),
    path("gastos/crear/", views.expense_create, name="expense_create"),
    path("gastos/<int:pk>/editar/", views.expense_update, name="expense_update"),
    path("gastos/<int:pk>/eliminar/", views.expense_delete, name="expense_delete"),
    path("reportes", views.reports, name="reports"),
    path("total", views.totals_by_month_year, name="totals_by_month_year"),
    path("excel", views.export_incomes_expenses_to_excel, name="export_excel"),
    # ex: /polls/5/
]
