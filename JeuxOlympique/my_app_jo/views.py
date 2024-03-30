from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import InscriptionForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Offre, Commande, Competitions, User ,List_competition,Billet,Competitions,Offre
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.shortcuts import render
import qrcode, base64
from django.db.models import Count, Sum,Q
from io import BytesIO

 


def home(request):
    competitions = Competitions.objects.all()
    return render(request, 'home.html', {'competitions': competitions})




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
        montant_total = commande.MontantTotal if commande else 0  # Assurez-vous d'adapter cela à votre modèle de données
        return render(request, 'payer_commande.html', {'commande_id': commande_id , 'montant_total': montant_total})
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
        nom_utilisateur = commande.pk_Utilisateur.username

    else:
        montant_total_commande = None
        type_offre = None
        nom_utilisateur = None
    
    # Concaténer la clef utilisateur et la clef de billet pour former le contenu du QR code
    qr_content = f"{billet.ClefUtilisateur}{billet.Cledebilletelectroniquesecurisee}"
    
    # Générer le QR code
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(qr_content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Enregistrer le QR code dans un buffer
    buffer = BytesIO()
    img.save(buffer, 'PNG')
    qr_image = base64.b64encode(buffer.getvalue()).decode()
    
    # Renvoyer le rendu de la page avec le billet, le QR code, et les informations supplémentaires
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

        # Vérifier si une commande existe pour ce billet
        if commande:
            # Créer le contenu du QR code avec la clé utilisateur et la clé du billet
            qr_content = f"{billet.ClefUtilisateur}{billet.Cledebilletelectroniquesecurisee}"
            
            # Générer le QR code
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(qr_content)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # Convertir l'image du QR code en base64
            buffer = BytesIO()
            img.save(buffer,"PNG")
            qr_image = base64.b64encode(buffer.getvalue()).decode()

            # Ajouter le billet avec ses informations et le QR code à la liste
            billets_with_qr.append({'billet': billet, 'commande': commande, 'qr_image': qr_image})

    return render(request, 'mes_billets.html', {'billets_with_qr': billets_with_qr})

def generate_qr_code(content):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, 'PNG')
    qr_image = base64.b64encode(buffer.getvalue()).decode()

    return qr_image

#Competition
def lister_competitions(request):
    competitions = Competitions.objects.all()
    return render(request, 'lister_competitions.html', {'competitions': competitions})

 #   
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
#admin
def ventes_par_offre(request):
    # Récupérer les offres avec le nombre de ventes pour chaque offre
    ventes_par_offre = Offre.objects.annotate(
        nombre_ventes=Count('commande', filter=Q(commande__est_validee=True)),
        quantite_vendue=Sum('commande__quantite', filter=Q(commande__est_validee=True))
    ).filter(
        commande__est_validee=True  # Commande validée
    ).annotate(
        montant_total_ventes=Sum('commande__MontantTotal')  # Calcul du montant total des ventes pour chaque offre
    )
     
    
    return render(request, 'admin/ventes_par_offre.html', {'ventes_par_offre': ventes_par_offre})
