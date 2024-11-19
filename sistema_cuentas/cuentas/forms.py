from django import forms
from .models import Income
from datetime import datetime
class IncomeForm(forms.ModelForm):
    name = forms.CharField(label="Nombre", max_length=100)
    value = forms.FloatField(label="Valor")
    date = forms.DateField(label="Fecha", initial=datetime.now())
    class Meta:
        model = Income
        fields = ['name', 'value', 'date']
