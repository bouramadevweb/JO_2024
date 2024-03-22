from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import InscriptionForm, CommandeForm
from django.contrib.auth.decorators import login_required
from .models import Offre, Commande, Competitions, User

def home(request):
    return render(request, 'home.html', {})

def choisir_ticket(request):
    offres = Offre.objects.all()
    return render(request, 'choisir_ticket.html', {'offres': offres})

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            messages.success(request, f'Félicitations, {user.email} ! Votre compte a été créé avec succès.')
            return redirect('choisir_ticket')
    else:
        form = InscriptionForm()
        
    return render(request, 'inscription.html', {'form': form})
        
def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Vous êtes maintenant connecté.")
                return redirect('choisir_ticket')
            else:
                messages.error(request, "L'adresse e-mail ou le mot de passe est incorrect.")
    else:
        form = AuthenticationForm()
    return render(request, 'connexion.html', {'form': form})

def deconnexion(request):
    logout(request)
    return redirect('home')

@login_required
def passer_commande(request, offre_id):
    offre = Offre.objects.get(pk_Offre=offre_id)

    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            quantite = form.cleaned_data['quantite']
            montant_total = offre.Prix * quantite
            commande = Commande.objects.create(
                quantite=quantite,
                MontantTotal=montant_total,
                pk_Offre=offre,
                pk_Utilisateur=request.user,
                pk_Competition=offre.pk_typ_competition
            )
            commande.pk_Billet.generer_cles()
            messages.success(request, "La commande a été passée avec succès!")
            return redirect('confirmation_commande')
    else:
        form = CommandeForm()

    return render(request, 'passer_commande.html', {'offre': offre, 'form': form})
