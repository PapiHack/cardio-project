from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django import forms
import re
from .models import DataToAnalyze
from biosppy import storage
from biosppy.signals import ecg
from cardioproject.settings import BASE_DIR
import os

# Create your views here.

regexMail = r"^[a-z0-9._-]+@[a-z0-9._-]+\.[a-z]{2,6}$"

def register(request):
    return render(request, 'cardiouser/register.html')

def forgot(request):
    return render(request, 'cardiouser/forgot.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='cardiouser.connexion')
def home(request):
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='cardiouser.connexion')
def profil(request):
    user = User.objects.get(username=request.user)
    return render(request, 'cardiouser/mon_profil.html', {'user': user})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='cardiouser.connexion')
def input_data(request):
    return render(request, 'cardiouser/input_data.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='cardiouser.connexion')
def upload_and_analyze(request):
    user = User.objects.get(username=request.user)
    id_user = user.id
    if request.method == 'POST':
        formulaire = forms.Form(request.POST, request.FILES)
        print(request.FILES['dataset'])
        if formulaire.is_valid():
            data_to_analyze = DataToAnalyze()
            data_to_analyze.user = id_user
            data_to_analyze.dataset = request.FILES['dataset']
            data_to_analyze.save()
            #Faire l'analyse, affichage des graphes et tout le tralala ici
            signal, mdata = storage.load_txt(os.path.join(BASE_DIR, 'media/' + str(data_to_analyze.dataset)))
            out = ecg.ecg(signal=signal, sampling_rate=1000., show=True)
            #return redirect(home)
    return redirect(home)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='cardiouser.connexion')
def update_user(request, id):
    user = User.objects.get(id=id)
    old_mdp = user.password
    if request.method == 'GET':
        return redirect(home)
    elif request.method == 'POST':
        errors = dict()
        formulaire = forms.Form(request.POST)
        form = request.POST
        if formulaire.is_valid():
            if(re.match(regexMail, form['email'])):
                if(not mail_exist_for_edit(form['email'], user.username)):
                    if(not pseudo_exist_for_edit(form['pseudo'], user.username)):
                        if(form['mdp'] == form['cmdp']):
                            user.username = form['pseudo']
                            user.first_name = form['prenom']
                            user.last_name = form['nom']
                            if(form['mdp'] == old_mdp):
                                user.password = form['mdp']
                            else:
                                user.set_password(form['mdp'])
                            user.email = form['email']
                            user.is_superuser = form['user']
                            user.save()
                            return redirect(home)
                        else:
                            errors['mdp'] = 'Les mots de passes doivent être identiques.'
                    else:
                        errors['pseudo'] = 'Ce nom d\'utilisateur existe déjà.'
                else:
                    errors['mail'] = 'Cette adresse email existe déjà.'
            else:
                errors['mail'] = 'Adresse email invalide.'
    return render(request, 'cardiouser/mon_profil.html', locals())

def mail_exist_for_edit(mail, user):
    users = User.objects.exclude(username=user)
    for user in users:
        if(mail == user.email):
            return True
    return False

def pseudo_exist_for_edit(pseudo, user):
    users = User.objects.exclude(username=user)
    for user in users:
        if(pseudo == user.username):
            return True
    return False