from django.urls import path

from . import views
app_name = "cuentas"
urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    path("test", views.test, name="test"),
    # ex: /polls/5/
]