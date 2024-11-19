from django.urls import path

from . import views
app_name = "cuentas"
urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    path("entradas", views.incomes, name="incomes"),
    path('entradas/<int:pk>/', views.income_detail, name='income_detail'),
    path('entradas/crear/', views.income_create, name='income_create'),
    path('entradas/<int:pk>/editar/', views.income_update, name='income_update'),
    path('entradas/<int:pk>/eliminar/', views.income_delete, name='income_delete'),
    # ex: /polls/5/
]