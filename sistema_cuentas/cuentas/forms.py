from django import forms
from .models import Income, Expense
from datetime import datetime


class IncomeForm(forms.ModelForm):
    name = forms.CharField(label="Nombre", max_length=100)
    category = forms.CharField(label="Categoría", max_length=100)
    value = forms.DecimalField(label="Valor")
    date = forms.DateField(label="Fecha", initial=datetime.now())

    class Meta:
        model = Income
        fields = ["name", "value", "date", "category"]


class ExpenseForm(forms.ModelForm):
    name = forms.CharField(label="Nombre", max_length=100)
    category = forms.CharField(label="Categoría", max_length=100)
    value = forms.DecimalField(label="Valor")
    date = forms.DateField(label="Fecha", initial=datetime.now())

    class Meta:
        model = Expense
        fields = ["name", "value", "date", "category"]


class ReportForm(forms.Form):
    year = forms.IntegerField(
        label="Year",
        min_value=1,
        max_value=9999,
        widget=forms.NumberInput(
            attrs={"class": "form-control w-full", "placeholder": "Enter year"}
        ),
    )
    month = forms.IntegerField(
        label="Month",
        min_value=1,
        max_value=12,
        widget=forms.NumberInput(
            attrs={"class": "form-control w-full", "placeholder": "Enter month (1-12)"}
        ),
    )
