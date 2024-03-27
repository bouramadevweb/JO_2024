from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import InscriptionForm, CommandeForm,ModifierCommandeForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Offre, Commande, Competitions, User ,List_competition,Billet
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db import transaction
from django.http import JsonResponse

def home(request):
    return render(request, 'home.html', {})


from django.shortcuts import render
from .models import Offre, Competitions


@login_required
def choisir_ticket(request):
    if request.method == 'GET' and 'competition' in request.GET:
        # Récupérer l'ID de la compétition sélectionnée par l'utilisateur
        competition_id = request.GET.get('competition')

        # Sélectionner les offres pour la compétition sélectionnée
        offres = Offre.objects.filter(competition_id=competition_id)

        # Sélectionner toutes les compétitions disponibles
        competitions = Competitions.objects.select_related('pk_lieu').all()
        
        return render(request, 'choisir_ticket.html', {'offres': offres, 'competitions': competitions})
    else:
        # Si aucune compétition n'a été sélectionnée, afficher toutes les compétitions disponibles
        competitions = Competitions.objects.select_related('pk_lieu').all()
        return render(request, 'choisir_ticket.html', {'competitions': competitions})
@login_required
def ajouter_au_panier(request):
    if request.method == 'POST':
        print("Données POST reçues :", request.POST)
        
        # Récupérer les données des offres sélectionnées
        offre_ids = request.POST.getlist('offre_id')
        quantites = {offre_id: int(request.POST.get(f'quantite_{offre_id}', 0)) for offre_id in offre_ids}
        
        # Vérifier la validité des données reçues
        if not offre_ids or any(quantites[offre_id] <= 0 for offre_id in offre_ids):
            messages.error(request, "Veuillez sélectionner au moins une offre et spécifier une quantité valide.")
            return redirect('choisir_ticket')

        try:
            with transaction.atomic():
                # Créer les commandes pour les offres sélectionnées
                for offre_id, quantite in quantites.items():
                    if quantite <= 0:
                        continue  # Ignorer les quantités nulles ou négatives
                    
                    # Récupérer l'offre correspondante
                    offre = Offre.objects.get(pk=offre_id)
                    
                    # Calculer le montant total
                    montant_total = (offre.prix) * quantite
                    
                    # Créer la commande avec le montant total calculé
                    commande = Commande.objects.create(
                        pk_Offre=offre,
                        quantite=quantite,
                        MontantTotal=montant_total,
                        pk_Utilisateur=request.user
                    )

                    # Générer le billet si la commande est validée
                    if commande.est_validee:
                        commande.save()  # Appel de la méthode pour générer le billet

                        print(f"Billet généré pour la commande {commande.pk_Commande}")

                messages.success(request, "Les offres ont été ajoutées au panier.")
                return redirect('voir_panier')
        except Exception as e:
            messages.error(request, f"Une erreur s'est produite lors de la validation de la commande : {str(e)}")
            print(f"Erreur lors de la validation de la commande : {str(e)}")
            return redirect('choisir_ticket')

    else:
        return redirect('choisir_ticket')

@login_required
def voir_panier(request):
    commandes = Commande.objects.filter(pk_Utilisateur=request.user)
    return render(request, 'voir_panier.html', {'commandes': commandes})
@login_required
def valider_commande(request):
    if request.method == 'POST':
        commandes_a_valider = Commande.objects.filter(pk_Utilisateur=request.user, est_validee=False)
        commandes_a_valider.update(est_validee=True)  # Marquer toutes les commandes comme validées
        messages.success(request, "Vos commandes ont été validées avec succès.")
    return redirect('voir_panier')

@login_required
def modifier_commande(request, commande_id):
    # Récupérer la commande correspondante
    commande = get_object_or_404(Commande, pk=commande_id)

    if request.method == 'POST':
        # Traitement des requêtes POST
        type_offre_id = request.POST.get('offre_id')
        quantite = int(request.POST.get('quantite'))

        # Récupérer l'offre correspondante
        offre = get_object_or_404(Offre, pk=type_offre_id)

        # Calculer le montant total de la commande
        montant_total = offre.prix * quantite

        # Mettre à jour la commande avec les nouvelles données
        Commande.objects.filter(pk=commande_id).update(
            pk_Offre=offre.pk_Offre,
            quantite=quantite,
            MontantTotal=montant_total
        )

        # Rediriger vers une autre vue après la modification
        return redirect('voir_panier')
    else:
        # Traitement des requêtes GET
        # Récupérer l'ID de la compétition sélectionnée par l'utilisateur (s'il y en a une)
        competition_id = request.GET.get('competition')

        # Sélectionner toutes les compétitions disponibles
        competitions = Competitions.objects.select_related('pk_lieu').all()

        # Sélectionner les offres en fonction de la compétition sélectionnée, ou toutes les offres si aucune compétition n'est sélectionnée
        if competition_id:
            offres = Offre.objects.filter(competition_id=competition_id)
        else:
            offres = Offre.objects.all()

        # Rendre le template avec les données nécessaires
        return render(request, 'modifier_commande.html', {
            'commande': commande,
            'offres': offres,
            'competitions': competitions,
            'selected_competition_id': competition_id  # Passer l'ID de la compétition sélectionnée au modèle
        })
    
def supprimer_commande(request, commande_id):
    commande = Commande.objects.get(pk=commande_id)
    commande.delete()
    messages.success(request, "La commande a été supprimée avec succès.")
    return redirect('voir_panier')   
 
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
def get_offres(request):
    if request.method == 'GET' and 'competition_id' in request.GET:
        competition_id = request.GET.get('competition_id')
        
        # Sélectionner les offres pour la compétition spécifiée
        offres = Offre.objects.filter(competition_id=competition_id)
        
        # Construire une liste de dictionnaires représentant les offres
        offres_data = []
        for offre in offres:
            offres_data.append({
                'pk_Offre': offre.pk_Offre,
                'type': offre.type,
                'nombre_personnes': offre.nombre_personnes,
                # Ajoutez d'autres champs d'offre si nécessaire
            })
        
        return JsonResponse(offres_data, safe=False)
    else:
        # Si la requête n'est pas valide, renvoyer une réponse d'erreur
        return JsonResponse({'error': 'Paramètres de requête invalides'}, status=400)