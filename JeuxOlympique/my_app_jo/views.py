from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm,UserChangeForm
from django.contrib import messages
from .forms import InscriptionForm,CustomUserChangeForm
# from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Offre, Commande, Competitions, User ,List_competition,Billet,Competitions,Offre
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.shortcuts import render
from datetime import datetime ,timezone
import qrcode, base64
from django.http import HttpResponse
# from django.db.models import Count, Sum,Q
# import secrets
import string
import random
from django.views.decorators.csrf import csrf_exempt
# from django.core.mail import send_mail
from django.contrib.auth.models import User
# from django.utils.crypto import get_random_string
from .models import User ,Code
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from .forms import VerificationCodeForm
from io import BytesIO
from .forms import BootstrapAuthenticationForm
from .utils import envoie_sms

def home(request):
    competitions = Competitions.objects.all()
    return render(request, 'home.html', {'competitions': competitions})

def choisir_ticket(request):
    if request.method == 'GET' and 'competition' in request.GET:
        # Récupérer l'ID de la compétition sélectionnée par l'utilisateur
        competition_id = request.GET.get('competition')

        # Récupérer le type sélectionné par l'utilisateur
        selected_type = request.GET.get('type')

        # Sélectionner les offres pour la compétition et le type sélectionnés
        if selected_type:
            page_objs = Offre.objects.filter(competition_id=competition_id, type__type=selected_type)
        else:
            page_objs = Offre.objects.filter(competition_id=competition_id)

        # Sélectionner toutes les compétitions disponibles
        competitions = Competitions.objects.select_related('pk_lieu').all()
        
        return render(request, 'choisir_ticket.html', {'page_objs': page_objs, 'competitions': competitions})
    else:
        # Si aucune compétition n'a été sélectionnée, afficher toutes les compétitions disponibles
        competitions = Competitions.objects.select_related('pk_lieu').all()
        return render(request, 'choisir_ticket.html', {'competitions': competitions})

@login_required
@csrf_exempt
def ajouter_au_panier(request):
    if request.method == 'POST':
        try:
            print("Données POST reçues :", request.POST)
            
            # Récupérer les données des offres sélectionnées
            offre_ids = request.POST.getlist('offre_id')
            quantites = {offre_id: int(request.POST.get(f'quantite_{offre_id}', 0)) for offre_id in offre_ids}
            print(offre_ids)
            print(offre_ids)
            # Vérifier la validité des données reçues
            if not offre_ids or any(quantites.get(offre_id, 0) <= 0 for offre_id in offre_ids):
                messages.error(request, "Veuillez sélectionner au moins une offre et spécifier une quantité valide.")
                return redirect('choisir_ticket')

            with transaction.atomic():
                for offre_id, quantite in quantites.items():
                    if quantite <= 0:
                        continue
                    
                    # Vérifier si l'offre existe
                    offre = Offre.objects.filter(pk=offre_id).first()
                    if not offre:
                        messages.error(request, f"L'offre avec l'ID {offre_id} n'existe pas.")
                        return redirect('choisir_ticket')
                    
                    # Récupérer la date de début de l'offre seulement si l'offre est sélectionnée
                    if offre_id in offre_ids:
                        date_debut_str = request.POST.get(f'date_debut_{offre_id}', None)
                        if date_debut_str:
                            date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d').date()
                        else:
                            messages.error(request, f"La date de début est manquante pour l'offre {offre_id}.")
                            return redirect('choisir_ticket')

                        # Calculer le montant total
                        montant_total = offre.prix * quantite

                        print(montant_total)
                        
                        # Créer la commande avec le montant total calculé
                        commande = Commande.objects.create(
                            quantite=quantite,
                            MontantTotal=montant_total,
                            pk_Offre=offre,
                            pk_Utilisateur=request.user,
                        )
                        print("Commande créée :", commande)  
                        
                        commande.save()
                        print(f"Commande créée avec succès pour l'offre {offre_id}")

                messages.success(request, "Les offres ont été ajoutées au panier.")
                return redirect('voir_panier')  
        except Exception as e:
            messages.error(request, f"Une erreur s'est produite lors de la validation de la commande : {str(e)}")
            print(f"Erreur lors de la validation de la commande : {str(e)}")
            return redirect('choisir_ticket')

    return redirect('choisir_ticket')

@login_required
def voir_panier(request):
    commandes = Commande.objects.filter(pk_Utilisateur=request.user)
    return render(request, 'voir_panier.html', {'commandes': commandes})

@login_required
def payer_commande(request, commande_id):
    # Récupérer la commande spécifique à payer
    commande = Commande.objects.filter(pk=commande_id, pk_Utilisateur=request.user, est_validee=False).first()
    
    if request.method == 'POST':
        # Simulation du paiement
        if commande:
            # Début de la transaction pour garantir l'intégrité des données
            with transaction.atomic():
                # Mettre à jour la commande comme validée dans la base de données
                Commande.objects.filter(pk=commande_id, pk_Utilisateur=request.user, est_validee=False).update(est_validee=True)
                Billet.objects.filter(pk=commande.pk_Billet_id).update(est_validee=True)
                
                # Rediriger vers la page de détails du billet avec l'ID du billet comme argument
                return redirect('details_billet', billet_id=commande.pk_Billet_id)
        else:
            messages.error(request, "La commande n'existe pas ou a déjà été validée.")
            return redirect('voir_panier')
    else:
        # Passer le montant total comme contexte vers le modèle HTML
        montant_total = commande.MontantTotal if commande else 0  
        return render(request, 'payer_commande.html', {'commande_id': commande_id , 'montant_total': montant_total})
@login_required
def modifier_commande(request, commande_id):
    # Récupérer la commande correspondante
    commande = get_object_or_404(Commande, pk=commande_id)

    if request.method == 'POST':
        # Traitement des requêtes POST
        type_offre_id = request.POST.get('offre_id')
        quantite_str = request.POST.get('quantite')

        # Débogage
        print("Valeur de quantite_str :", quantite_str)

        if quantite_str:
            try:
                quantite = int(quantite_str)
            except ValueError:
                # Gérer le cas où la quantité n'est pas un entier valide
                return HttpResponse("La quantité doit être un entier.")
        else:
            # Gérer le cas où la clé 'quantite' n'est pas présente dans la requête POST
            return HttpResponse("La quantité n'a pas été spécifiée.")

        # Récupérer l'offre correspondante
        offre = get_object_or_404(Offre, pk=type_offre_id)

        # Calculer le montant total de la commande
        montant_total = offre.prix * quantite

        # Mettre à jour la commande avec les nouvelles données
        commande.pk_Offre = offre
        commande.quantite = quantite
        commande.MontantTotal = montant_total
        commande.save()

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
 

def details_billet(request, billet_id):
    billet = get_object_or_404(Billet, pk=billet_id)
    
    # Récupérer la commande associée au billet
    commande = billet.commande_set.first()
    
    # Vérifier si une commande existe
    if commande:
        # Récupérer le montant total de la commande
        montant_total_commande = commande.MontantTotal
        
        # Récupérer le type d'offre
        type_offre = commande.pk_Offre.type
        
        # Récupérer le nom de l'utilisateur
        nom_utilisateur = commande.pk_Utilisateur.first_name

    else:
        montant_total_commande = None
        type_offre = None
        nom_utilisateur = None
    
    # Concaténer la clé utilisateur et la clé de billet pour former le contenu du QR code
    qr_content = f"{billet.ClefUtilisateur}{billet.Cledebilletelectroniquesecurisee} {commande.pk_Utilisateur.first_name} {commande.pk_Utilisateur.last_name} {commande.pk_Utilisateur.username}"
    
    # Générer le QR code
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(qr_content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Enregistrer le QR code dans un buffer
    buffer = BytesIO()
    img.save(buffer, 'PNG')
    qr_image = base64.b64encode(buffer.getvalue()).decode()
    
    # Renvoyer le rendu de la page avec le billet, le QR code et les informations supplémentaires
    return render(request, 'details_billet.html', {'billet': billet, 'qr_image': qr_image, 
                                                   'montant_total_commande': montant_total_commande,
                                                   'type_offre': type_offre,
                                                   'nom_utilisateur': nom_utilisateur})

def mes_billets(request):
    # Récupérer tous les billets avec les informations de commande associées
    billets_with_qr = []

    billets = Billet.objects.all()

    for billet in billets:
        # Récupérer la commande associée à ce billet
        commande = Commande.objects.filter(pk_Billet=billet.pk_Billet).first()

        # Vérifier si une commande existe pour ce billet et si elle est valide
        if commande and commande.est_validee:
            # Créer le contenu du QR code avec la clé utilisateur et la clé du billet
            qr_content = f"{billet.ClefUtilisateur}{billet.Cledebilletelectroniquesecurisee} {commande.pk_Utilisateur.first_name} {commande.pk_Utilisateur.last_name}"
            
            # Générer le QR code
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(qr_content)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # Convertir l'image du QR code en base64
            buffer = BytesIO()
            img.save(buffer, "PNG")
            qr_image = base64.b64encode(buffer.getvalue()).decode()

            # Ajouter le billet avec ses informations et le QR code à la liste
            billets_with_qr.append({'billet': billet, 'commande': commande, 'qr_image': qr_image})

    return render(request, 'mes_billets.html', {'billets_with_qr': billets_with_qr})


def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            messages.success(request, f'Félicitations, {user.email} ! Votre compte a été créé avec succès.')
            request.session['user_pk'] = user.pk 
            return redirect('verificode')
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
                request.session['user_pk'] = user.pk
                
                # Vérifier si le code associé à l'utilisateur est déjà valide
                code = user.code
                if code.est_validee:
                    # Générer un nouveau code en mettant à jour le numéro du code existant
                    while True:
                        new_code = ''.join(random.choices(string.digits, k=5))
                        if not Code.objects.filter(number=new_code).exists():
                            code.number = new_code
                            code.save()
                            messages.info(request, "Un nouveau code de vérification a été envoyé à votre téléphone.")
                            break
                
                return redirect('verificode')  
            else:
                messages.error(request, "L'adresse e-mail ou le mot de passe est incorrect.")
    else:      
        form = BootstrapAuthenticationForm()
    return render(request, 'connexion.html', {'form': form})


def verificode(request):
    form = VerificationCodeForm(request.POST or None)
    user_pk = request.session.get('user_pk')  # Récupérer la clé primaire de l'utilisateur depuis la session
    if user_pk:
        user = User.objects.get(pk=user_pk)
        code = user.code
        code_user = f'{user.username} {user.phone_number}'
        print(code_user)
        
        # Envoi du SMS de vérification dans tous les cas
        envoie_sms(code.number, user.phone_number)
        
        if request.method == 'POST':
            if form.is_valid():
                num = form.cleaned_data.get('verification_code')
                if str(code) == num:
                    # Vérifier si le code est valide et non utilisé
                    if not code.est_validee:
                        # Appeler la méthode verifier() du code
                        code.verifier()
                        # Connecter l'utilisateur
                        user.save()
                        login(request, user)
                        messages.success(request, "Connexion réussie.")
                        return redirect('home')
                    else:
                        messages.error(request, "Code déjà utilisé.")
                        return redirect('inscription')  # Rediriger vers la page d'inscription si le code est déjà utilisé
                else:
                    messages.error(request, "Code incorrect. Redirection vers la page d'inscription.")
                    return redirect('inscription')
    return render(request, 'saisie_code_verification.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'profile.html', context)
@login_required
def modifier_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'modifier_profile.html', {'form': form})
def deconnexion(request):
    logout(request)
    return redirect('home')

def handler404(request, exception):
    return render(request, '404.html', status=404)