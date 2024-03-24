from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import InscriptionForm, CommandeForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Offre, Commande, Competitions, User ,List_competition
from django.http import JsonResponse
from django.contrib import messages
import json

def home(request):
    return render(request, 'home.html', {})

from django.shortcuts import render
from .models import Offre, Competitions

def choisir_ticket(request):
    if request.method == 'POST':
        competition_id = request.POST.get('Competitions')
        if competition_id:
            offres = Offre.objects.filter(competition_id=competition_id)
        else:
            offres = None
    else:
        offres = None

    competitions = Competitions.objects.select_related('pk_lieu').all()
    return render(request, 'choisir_ticket.html', {'offres': offres, 'competitions': competitions})




# def ajouter_au_panier(request):
#     if request.method == 'POST':
#         offre_ids = request.POST.getlist('offre_id')
#         if offre_ids:
#             # Vérifier si le panier existe dans la session, sinon le créer
#             panier = request.session.get('panier', [])
#             # Ajouter les offres au panier si elles ne sont pas déjà présentes
#             for offre_id in offre_ids:
#                 if offre_id not in panier:
#                     panier.append(offre_id)
#             request.session['panier'] = panier
#             return JsonResponse({'success': True})
#         else:
#             return JsonResponse({'success': False, 'message': "ID d'offre manquant"})
#     else:
#         return JsonResponse({'success': False, 'message': "La requête doit être de type POST"})
def get_offres(request):
    competition_id = request.GET.get('competition_id')
    if competition_id:
        offres = Offre.objects.filter(competition_id=competition_id).values('pk_Offre', 'type', 'nombre_personnes', 'prix')
        return JsonResponse(list(offres), safe=False)
    else:
        return JsonResponse({'error': 'ID de compétition manquant'}, status=400)

from django.http import JsonResponse
from .models import Offre

# def ajouter_au_panier(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         offre_ids = data.get('offre_ids', [])
#         if offre_ids:
#             panier = request.session.get('panier', [])
#             for offre_id in offre_ids:
#                 if offre_id not in panier:
#                     panier.append(offre_id)
#             request.session['panier'] = panier
#             return JsonResponse({'success': True})
#         else:
#             return JsonResponse({'success': False, 'message': "Aucune offre sélectionnée."})
#     else:
#         return JsonResponse({'success': False, 'message': "La requête doit être de type POST."})
def ajouter_au_panier(request):
    if request.method == 'POST':
        # Récupérer les données de la requête AJAX
        data = request.POST  # Pour les données de formulaire POST
        # ou
        # data = json.loads(request.body)  # Pour les données JSON

        # Traitez les données et ajoutez-les au panier
        # Exemple :
        offre_id = data.get('offre_id')
        # Ajoutez l'offre_id au panier...

        # Retournez une réponse JSON indiquant le succès
        return JsonResponse({'success': True})
    else:
        # Si la requête n'est pas de type POST, retournez une réponse avec un message d'erreur
        return JsonResponse({'success': False, 'message': 'La requête doit être de type POST'})
def voir_panier(request):
    # Récupérer les éléments du panier depuis la session de l'utilisateur
    panier = request.session.get('panier', [])

    # Récupérer les offres correspondant aux identifiants dans le panier
    offres = Offre.objects.filter(pk_Offre__in=panier)

    return render(request, 'voir_panier.html', {'panier': panier, 'offres': offres})
 
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
