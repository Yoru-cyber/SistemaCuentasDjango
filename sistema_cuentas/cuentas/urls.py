from django.urls import path

from . import views
app_name = "cuentas"
urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    path("entradas", views.incomes, name="incomes"),
    # ex: /polls/5/
]