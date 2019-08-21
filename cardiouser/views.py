from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django import forms

# Create your views here.

regexMail = r"^[a-z0-9._-]+@[a-z0-9._-]+\.[a-z]{2,6}$"

def register(request):
    return render(request, 'cardiouser/register.html')

def forgot(request):
    return render(request, 'cardiouser/forgot.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='cardiouser.connexion')
def home(request):
    print(request.user)
    return render(request, 'cardiouser/home.html')

def connexion(request):
    auth = False
    if request.method == 'POST':
        formulaire = forms.Form(request.POST)
        form = request.POST
        if formulaire.is_valid():
            username = form['login']
            mdp = form['mdp']
            try:
                p_user = User.objects.get(username=username)
            except:
                p_user = False
            user = authenticate(request, username=username, password=mdp)
            if user is not None and p_user.is_superuser is False:
                login(request, user)
                return redirect(home)
            else:
                auth = True
    return render(request, 'cardiouser/login.html', {'auth': auth})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='cardiouser.connexion')
def deconnexion(request):
    logout(request)
    return redirect(connexion)