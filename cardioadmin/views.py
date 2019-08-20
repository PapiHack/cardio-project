from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django import forms

# Create your views here.

regexMail = r"^[a-z0-9._-]+@[a-z0-9._-]+\.[a-z]{2,6}$"

def connexion(request):
    auth = False
    if request.method == 'POST':
        formulaire = forms.Form(request.POST)
        form = request.POST
        if formulaire.is_valid():
            username = form['login']
            mdp = form['mdp']
            try:
                admin = User.objects.get(username=username)
            except:
                admin = False
            user = authenticate(request, username=username, password=mdp)
            if user is not None and user.is_superuser and admin is not False:
                login(request, user)
                return redirect(home)
            else:
                auth = True
    return render(request, 'cardioadmin/login.html', {'auth': auth})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='cardioadmin.connexion')
def home(request):
    admin = User.objects.get(username=request.user)
    request.session['pseudo'] = admin.username
    request.session['totalUser'] = len(User.objects.all())
    request.session['users'] = len(User.objects.filter(is_superuser=False))
    request.session['admins'] = len(User.objects.filter(is_superuser=True))
    return render(request, 'cardioadmin/home.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='cardioadmin.connexion')
def deconnexion(request):
    logout(request)
    return redirect(connexion)

def forgot(request):
    return render(request, 'cardioadmin/forgot.html')
