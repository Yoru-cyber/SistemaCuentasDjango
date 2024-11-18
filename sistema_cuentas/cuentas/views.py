from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    context = {}
    return render(request, "cuentas/index.html", context)
def test(request):
    context = {}
    return HttpResponse("hello")