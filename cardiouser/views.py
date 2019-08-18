from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def login(request):
    return render(request, 'cardiouser/login.html')

def register(request):
    return render(request, 'cardiouser/register.html')

def forgot(request):
    return render(request, 'cardiouser/forgot.html')

def home(request):
    return render(request, 'cardiouser/home.html')

def connexion(request):
    pass

def deconnexion(request):
    pass
