from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django import forms
import re
from django.core.mail import send_mail
from django.template import loader
from django.urls import reverse

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
def profil(request):
    user = User.objects.get(username=request.user)
    return render(request, 'cardioadmin/mon_profil.html', locals())

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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='cardioadmin.connexion')
def gestion_admin(request):
    admins = User.objects.filter(is_superuser=True)
    return render(request, 'cardioadmin/gestion_admin.html', {'admins': admins})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='cardioadmin.connexion')
def gestion_user(request):
    users = User.objects.filter(is_superuser=False)
    return render(request, 'cardioadmin/gestion_user.html', {'users': users})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='cardioadmin.connexion')
def supprimer_user(request, id):
    user = User.objects.get(id=id)
    is_admin = user.is_superuser
    user.delete()
    if(is_admin):
        return redirect(gestion_admin)
    return redirect(gestion_user)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='cardioadmin.connexion')
def ajout_user(request, user):
    admin = False
    if(user == 'admin'):
        admin = True
    return render(request, 'cardioadmin/ajout_user.html', {'admin': admin})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='cardioadmin.connexion')
def add_user(request):
    if request.method == 'GET':
        return redirect(home)
    elif request.method == 'POST':
        errors = dict()
        formulaire = forms.Form(request.POST)
        form = request.POST
        if formulaire.is_valid():
            if(re.match(regexMail, form['email'])):
                if(not mail_exist(form['email'])):
                    if(not pseudo_exist(form['pseudo'])):
                        if(form['mdp'] == form['cmdp']):
                            user = User()
                            user.username = form['pseudo']
                            user.first_name = form['prenom']
                            user.last_name = form['nom']
                            user.set_password(form['mdp'])
                            user.email = form['email']
                            user.is_superuser = form['user']
                            user.save()
                            superuser = form['user']
                            if(superuser):
                                link = request.build_absolute_uri(reverse(connexion, None))
                                template = loader.get_template('cardioadmin/mailNewUser.txt')
                                t = template.render({'nom':user.last_name, 'prenom':user.first_name, 'link':link, 'statut':'Administrateur', 'login': user.username, 'mdp': form['mdp']})
                                send_mail('Vos informations d\'authentification', t, '', [user.email,], fail_silently=True)
                            else:
                                import cardiouser
                                link = request.build_absolute_uri(reverse(cardiouser.views.connexion, None))
                                template = loader.get_template('cardioadmin/mailNewUser.txt')
                                t = template.render({'nom':user.last_name, 'prenom':user.first_name, 'link':link, 'statut':'Utilisateur', 'login': user.username, 'mdp': form['mdp']})
                                send_mail('Vos informations d\'authentification', t, '', [user.email,], fail_silently=True)
                            #Envoyer les infos par mail au user
                            if(user.is_superuser):
                                return redirect(gestion_admin)
                            else:
                                return redirect(gestion_user)
                        else:
                            errors['mdp'] = 'Les mots de passes doivent être identiques.'
                    else:
                        errors['pseudo'] = 'Ce nom d\'utilisateur existe déjà.'
                else:
                    errors['mail'] = 'Cette adresse email existe déjà.'
            else:
                errors['mail'] = 'Adresse email invalide.'
    return render(request, 'cardioadmin/ajout_user.html', {'admin': form['user'], 'data': form, 'errors': errors})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='cardioadmin.connexion')
def edit_user(request, id):
    user = User.objects.get(id=id)
    admin = user.is_superuser
    return render(request, 'cardioadmin/edit_user.html', locals())

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='cardioadmin.connexion')
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
                            #Envoyer les infos par mail au user
                            if(user.is_superuser):
                                return redirect(gestion_admin)
                            else:
                                return redirect(gestion_user)
                        else:
                            errors['mdp'] = 'Les mots de passes doivent être identiques.'
                    else:
                        errors['pseudo'] = 'Ce nom d\'utilisateur existe déjà.'
                else:
                    errors['mail'] = 'Cette adresse email existe déjà.'
            else:
                errors['mail'] = 'Adresse email invalide.'
    return render(request, 'cardioadmin/edit_user.html', locals())

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

def pseudo_exist(pseudo):
    for user in User.objects.all():
        if(pseudo == user.username):
            return True
    return False

def mail_exist(mail):
    for user in User.objects.all():
        if(mail == user.email):
            return True
    return False