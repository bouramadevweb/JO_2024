from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import InscriptionForm, CommandeForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Offre, Commande, Competitions, User ,List_competition,Billet
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction

def home(request):
    return render(request, 'home.html', {})


from django.shortcuts import render
from .models import Offre, Competitions

def choisir_ticket(request):
    # Sélectionner la première compétition disponible
    competitions = Competitions.objects.select_related('pk_lieu').all()
    if competitions:
        competition_id = competitions.first().pk_typ_competition
        offres = Offre.objects.filter(competition_id=competition_id)
    else:
        offres = None

    return render(request, 'choisir_ticket.html', {'offres': offres, 'competitions': competitions})

@login_required
def ajouter_au_panier(request):
    if request.method == 'POST':
        offre_ids = request.POST.getlist('offre_id')
        quantites = {offre_id: int(request.POST.get(f'quantite_{offre_id}', 0)) for offre_id in offre_ids}
        
        # Vérifier la validité de la commande
        if not offre_ids or any(quantites[offre_id] <= 0 for offre_id in offre_ids):
            messages.error(request, "Veuillez sélectionner au moins une offre et spécifier une quantité valide.")
            return redirect('choisir_ticket')

        # Créer la commande
        try:
            with transaction.atomic():
                for offre_id, quantite in quantites.items():
                    offre = Offre.objects.get(pk=offre_id)
                    # Valider la disponibilité des offres ou d'autres critères si nécessaire
                    if quantite <= 0:
                        continue  # Ignorer les quantités nulles ou négatives
                    commande = Commande.objects.create(
                        offre=offre,
                        quantite=quantite,
                        MontantTotal=offre.prix * quantite,
                        pk_Utilisateur=request.user
                    )

                    # Générer le billet
                    billet = Billet.objects.create(
                        pk_typ_competition=offre.competition
                        # Autres champs du billet
                    )
                    commande.pk_Billet = billet
                    commande.save()

                    print(f"Billet généré pour la commande {commande.pk_Commande}")

                messages.success(request, "Les offres ont été ajoutées au panier.")
                return redirect('voir_panier')
        except Exception as e:
            messages.error(request, f"Une erreur s'est produite lors de la validation de la commande : {str(e)}")
            return redirect('choisir_ticket')

    else:
        return redirect('choisir_ticket')


@login_required
def voir_panier(request):
    commandes = Commande.objects.filter(pk_Utilisateur=request.user)
    return render(request, 'voir_panier.html', {'commandes': commandes})

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
