from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Offre, Commande, Competitions
import secrets
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import logout

class InscriptionForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

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
            # Générer un token et l'associer à l'utilisateur
            user.token = secrets.token_hex(16)  # Générer un token de 16 octets
            user.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Félicitations, {email} ! Votre compte a été créé avec succès.')
            return redirect('connexion')
    else:
        form = InscriptionForm()
    return render(request, 'inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # 'username' correspond à l'email par défaut dans AuthenticationForm
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('choisir_ticket')
            else:
                messages.error(request, "L'adresse e-mail ou le mot de passe est incorrect.")
    else:
        form = AuthenticationForm()
    return render(request, 'connexion.html', {'form': form})

def deconnexion(request):
    logout(request)
    return redirect('home')

def passer_commande(request, offre_id):
    if request.method == 'POST':
        offre = Offre.objects.get(pk_Offre=offre_id)
        quantite = request.POST['quantite']
        montant_total = offre.Prix * int(quantite)
        user = request.user
        competition_id = request.POST.get('competition')
        commande = Commande.objects.create(
            quantite=quantite,
            MontantTotal=montant_total,
            pk_Offre=offre,
            pk_Utilisateur=user,
            pk_Competition=competition_id
        )
        
        request.session['panier'] = request.session.get('panier', [])
        request.session['panier'].append({
            'offre_id': offre_id,
            'quantite': quantite,
            'pk_competition': competition_id
        })
        request.session.modified = True
        return render(request, 'confirmation_commande.html', {'commande': commande})
    else:
        offre = Offre.objects.get(pk_Offre=offre_id)
        competitions = Competitions.objects.all()  
        return render(request, 'passer_commande.html', {'offre': offre, 'competitions': competitions})
