from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def login(request):
    return render(request, 'cardioadmin/login.html')

def connexion(request):
    pass

def home(request):
    return render(request, 'cardioadmin/home.html')

def deconnexion(request):
    pass

def forgot(request):
    return render(request, 'cardioadmin/forgot.html')
