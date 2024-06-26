from django.test import TestCase,Client
from django.test import TestCase, RequestFactory
from .models import Competitions,Code ,Types,Lieu_des_competions,List_competition,Dates_Competions,Offre,Commande,User,Billet
from datetime import datetime
from unittest.mock import patch
from io import BytesIO
import base64
import pytest
from django.contrib.messages import get_messages
from django.utils import timezone
from my_app_jo.views import choisir_ticket
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from .views import ajouter_au_panier,modifier_profile,offresuser
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib import messages
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from my_app_jo.forms import CustomUserChangeForm  
from django.contrib.auth import get_user_model
from .models import Offre, Commande, Billet, Competitions
from .views import choisir_ticket, ajouter_au_panier
import string
import secrets

from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from my_app_jo.models import User  
from my_app_jo.views import ajouter_au_panier
from my_app_jo.models import Commande, Billet, Offre, Competitions
from django.http import QueryDict
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from my_app_jo.views import voir_panier
from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, choisir_ticket, ajouter_au_panier, voir_panier, payer_commande, modifier_commande, supprimer_commande, details_billet, mes_billets, inscription, connexion, deconnexion #, ventes_par_offre


User = get_user_model()
class ListCompetitionCRUDTestCase(TestCase):
    """
        test List des competitions   
    """
    def setUp(self):
        # Créer une instance de List_competition pour les tests
        self.football_competition = List_competition.objects.create(pk_list_competition='Football', 
                                                                    nom='Football')

    def test_create_list_competition(self):
        # Vérifier si l'instance de List_competition a été créée avec succès
        new_competition = List_competition.objects.create(pk_list_competition='Basketball',
                                                           nom='Basketball')
        self.assertEqual(new_competition.nom, 'Basketball')

    def test_read_list_competition(self):
        # Vérifier si l'instance de List_competition peut être récupérée avec succès
        retrieved_competition = List_competition.objects.get(pk_list_competition='Football')
        self.assertEqual(retrieved_competition.nom, 'Football')

    def test_update_list_competition(self):
        # Modifier l'instance de List_competition
        self.football_competition.nom = 'Soccer'
        self.football_competition.save()

        # Vérifier si la modification a été correctement enregistrée
        updated_competition = List_competition.objects.get(pk_list_competition='Football')
        self.assertEqual(updated_competition.nom, 'Soccer')

    def test_delete_list_competition(self):
        # Supprimer l'instance de List_competition
        self.football_competition.delete()

        # Vérifier si l'instance a été supprimée avec succès
        with self.assertRaises(List_competition.DoesNotExist):
            List_competition.objects.get(pk_list_competition='Football')

class LieuDesCompetionsCRUDTestCase(TestCase):
    """Lieu_des_competions
    """
    def setUp(self):
        # Créer une instance de List_competition pour les tests
        self.list_competition = List_competition.objects.create(pk_list_competition='Football', 
                                                                nom='Football')

        # Créer une instance de Lieu_des_competions pour les tests
        self.lieu_des_competions = Lieu_des_competions.objects.create(
            pk_lieu='Paris_Stade_10000_Football',
            Nom='Stade de Paris',
            Ville='Paris',
            Capacite=10000,
            Discipline=self.list_competition
        )

    def test_create_lieu_des_competions(self):
        # Vérifier si l'instance de Lieu_des_competions a été créée avec succès
        new_lieu = Lieu_des_competions.objects.create(
            pk_lieu='London_Arena_15000_Football',
            Nom='London Arena',
            Ville='London',
            Capacite=15000,
            Discipline=self.list_competition
        )
        self.assertEqual(new_lieu.Nom, 'London Arena')

    def test_read_lieu_des_competions(self):
        # Vérifier si l'instance de Lieu_des_competions peut être récupérée avec succès
        retrieved_lieu = Lieu_des_competions.objects.get(pk_lieu='Paris_Stade_10000_Football')
        self.assertEqual(retrieved_lieu.Nom, 'Stade de Paris')

    def test_update_lieu_des_competions(self):
        # Modifier l'instance de Lieu_des_competions
        self.lieu_des_competions.Nom = 'Paris Stadium'
        self.lieu_des_competions.save()

        # Vérifier si la modification a été correctement enregistrée
        updated_lieu = Lieu_des_competions.objects.get(pk_lieu='Paris_Stade_10000_Football')
        self.assertEqual(updated_lieu.Nom, 'Paris Stadium')

    def test_delete_lieu_des_competions(self):
        # Supprimer l'instance de Lieu_des_competions
        self.lieu_des_competions.delete()

        # Vérifier si l'instance a été supprimée avec succès
        with self.assertRaises(Lieu_des_competions.DoesNotExist):
            Lieu_des_competions.objects.get(pk_lieu='Paris_Stade_10000_Football')  

class DatesCompetionsCRUDTestCase(TestCase):
    """ test  Dates_Competions
    """
    def setUp(self):
        # Créer des instances de List_competition et Lieu_des_competions pour les tests
        self.list_competition = List_competition.objects.create(pk_list_competition='Football', 
                                                                nom='Football')
        self.lieu_des_competions = Lieu_des_competions.objects.create(pk_lieu='Paris_Stade_10000_Football',
                                                                      Nom='Stade de Paris',
                                                                      Ville='Paris',
                                                                      Capacite=10000,
                                                                      Discipline=self.list_competition)

        # Créer une instance de Dates_Competions pour les tests
        self.dates_competions = Dates_Competions.objects.create(
            pk_date_competition='Football_Paris_Stade_2024-08-01_2024-08-11',
            date_debut=datetime(2024, 8, 1),
            date_fin=datetime(2024, 8, 11),
            pk_list_competition=self.list_competition,
            pk_lieu=self.lieu_des_competions,
            Remises_de_medailles='Some medals'
        )

    def test_create_dates_competions(self):
        # Créer une instance de Dates_Competions
        new_dates_competions = Dates_Competions.objects.create(
            date_debut=datetime(2024, 8, 12),
            date_fin=datetime(2024, 8, 20),
            pk_list_competition=self.list_competition,
            pk_lieu=self.lieu_des_competions,
            Remises_de_medailles='Some other medals'
        )

        # Récupérer l'instance nouvellement créée à partir de la base de données
        saved_dates_competions = Dates_Competions.objects.get(pk_date_competition=new_dates_competions.pk_date_competition)

        # Comparer la clé primaire de l'instance nouvellement créée avec la valeur attendue
        self.assertEqual(saved_dates_competions.pk_date_competition, new_dates_competions.pk_date_competition)

    def test_read_dates_competions(self):
        # Récupérer l'instance créée dans setUp
        retrieved_dates_competions = self.dates_competions

        # Vérifier si l'instance récupérée a les attributs attendus
        self.assertEqual(retrieved_dates_competions.date_debut, datetime(2024, 8, 1))
        self.assertEqual(retrieved_dates_competions.date_fin, datetime(2024, 8, 11))
        self.assertEqual(retrieved_dates_competions.pk_list_competition.pk_list_competition, 'Football')  # Vérifier la clé primaire de la compétition
        self.assertEqual(retrieved_dates_competions.pk_lieu.pk_lieu, 'Paris_Stade_10000_Football')  # Vérifier la clé primaire du lieu
        self.assertEqual(retrieved_dates_competions.Remises_de_medailles, 'Some medals')

    def test_update_dates_competions(self):
        # Modifier l'instance de Dates_Competions
        self.dates_competions.Remises_de_medailles = 'Some new medals'
        self.dates_competions.save()

        # Récupérer l'instance mise à jour à partir de la base de données
        updated_dates_competions = Dates_Competions.objects.get(pk_date_competition=self.dates_competions.pk_date_competition)

        # Vérifier si la mise à jour a été effectuée avec succès
        self.assertEqual(updated_dates_competions.Remises_de_medailles, 'Some new medals')

    def test_delete_dates_competions(self):
        # Supprimer l'instance de Dates_Competions
        self.dates_competions.delete()

        # Vérifier si l'instance a été supprimée avec succès
        with self.assertRaises(Dates_Competions.DoesNotExist):
            Dates_Competions.objects.get(pk_date_competition='Football_Paris_Stade_2024-08-01_2024-08-11')

class CompetitionsCRUDTestCase(TestCase):
    """ test  Competitions
    """
    def setUp(self):
        # Création des instances nécessaires pour les tests
        self.list_competition = List_competition.objects.create(pk_list_competition='Football', nom='Football')
        self.lieu_des_competions = Lieu_des_competions.objects.create(pk_lieu='Paris_Stade_10000_Football', Nom='Stade de Paris', Ville='Paris', Capacite=10000, Discipline=self.list_competition)
        self.dates_competions = Dates_Competions.objects.create(pk_date_competition='Football_Paris_Stade_2024-08-01_2024-08-11', date_debut=datetime(2024, 8, 1), date_fin=datetime(2024, 8, 11), pk_list_competition=self.list_competition, pk_lieu=self.lieu_des_competions, Remises_de_medailles='Some medals')

    def test_competitions_CRUD(self):
    # Test de création
        new_competition = Competitions.objects.create(
        Nom='Test Competition',
        pk_list_competition=self.list_competition,
        pk_date_competition=self.dates_competions,
        pk_lieu=self.lieu_des_competions
       )
        self.assertIsNotNone(new_competition.pk_typ_competition)

    # Test de lecture
        retrieved_competition = Competitions.objects.get(pk_typ_competition=new_competition.pk_typ_competition)
        self.assertEqual(retrieved_competition.Nom, 'Test Competition')

    # Test de mise à jour
        Competitions.objects.filter(pk_typ_competition=new_competition.pk_typ_competition).update(Nom='Updated Competition')

    # Récupérer à nouveau l'objet mis à jour
        updated_competition = Competitions.objects.get(pk_typ_competition=new_competition.pk_typ_competition)
        self.assertEqual(updated_competition.Nom, 'Updated Competition')

    # Test de suppression
        updated_competition.delete()
        with self.assertRaises(Competitions.DoesNotExist):
            Competitions.objects.get(pk_typ_competition=new_competition.pk_typ_competition)
class TypesModelTestCase(TestCase):

    def setUp(self):
        # Configuration initiale pour vos tests
        Types.objects.create(type="Standard")
        Types.objects.create(type="Premium")

    def test_create_types(self):
        # Test pour vérifier la création des instances de Types
        deluxe = Types.objects.create(type="Deluxe")
        self.assertEqual(deluxe.type, "Deluxe")
        self.assertEqual(Types.objects.count(), 3)

    def test_read_types(self):
        # Test pour vérifier la lecture des instances de Types
        standard = Types.objects.get(type="Standard")
        premium = Types.objects.get(type="Premium")
        self.assertEqual(standard.type, "Standard")
        self.assertEqual(premium.type, "Premium")

    def test_update_types(self):
        # Test pour vérifier la mise à jour des instances de Types
        standard = Types.objects.get(type="Standard")
        standard.type = "Standard Plus"
        standard.save()
        self.assertEqual(Types.objects.get(pk="Standard Plus").type, "Standard Plus")

    def test_delete_types(self):
        # Test pour vérifier la suppression des instances de Types
        standard = Types.objects.get(type="Standard")
        standard.delete()
        self.assertEqual(Types.objects.count(), 1)
        with self.assertRaises(Types.DoesNotExist):
            Types.objects.get(type="Standard")

    def test_types_str(self):
        # Test pour vérifier la méthode __str__
        standard = Types.objects.get(type="Standard")
        premium = Types.objects.get(type="Premium")
        self.assertEqual(str(standard), "Standard")
        self.assertEqual(str(premium), "Premium")


class OffreCRUDTestCase(TestCase):
    """Test Offre
    """
    def setUp(self):
        # Création des instances 
        self.list_competition = List_competition.objects.create(pk_list_competition='Football', nom='Football')
        self.lieu_des_competions = Lieu_des_competions.objects.create(pk_lieu='Paris_Stade_10000_Football', Nom='Stade de Paris', Ville='Paris', Capacite=10000, Discipline=self.list_competition)
        self.dates_competions = Dates_Competions.objects.create(pk_date_competition='Football_Paris_Stade_2024-08-01_2024-08-11', date_debut=datetime(2024, 8, 1), date_fin=datetime(2024, 8, 11), pk_list_competition=self.list_competition, pk_lieu=self.lieu_des_competions, Remises_de_medailles='Some medals')
        self.competition = Competitions.objects.create(Nom='Test Competition', pk_list_competition=self.list_competition, pk_date_competition=self.dates_competions, pk_lieu=self.lieu_des_competions)
        self.type  = Types.objects.create(type = 'One')
    def test_offre_CRUD(self):
        type_duo, created = Types.objects.get_or_create(type='Duo')
        # Test de création
        new_offre = Offre.objects.create(
            type= self.type,
            nombre_personnes=1,
            prix=10.0,
            competition=self.competition
        )
        self.assertIsNotNone(new_offre.pk_Offre)

        # Test de lecture
        retrieved_offre = Offre.objects.get(pk_Offre=new_offre.pk_Offre)
        self.assertEqual(retrieved_offre.type.type,'One')

        # Test de mise à jour
        retrieved_offre.type = type_duo
        retrieved_offre.save()

        # Récupérer à nouveau l'objet mis à jour
        updated_offre = Offre.objects.get(pk_Offre=new_offre.pk_Offre)
        self.assertEqual(updated_offre.type.type, 'Duo')

        # Test de suppression
        updated_offre.delete()
        with self.assertRaises(Offre.DoesNotExist):
            Offre.objects.get(pk_Offre=new_offre.pk_Offre)

class BilletCRUDTestCase(TestCase):
    """test Billet
    """

    def setUp(self):
        # Créer des instances nécessaires pour Competitions
        list_competition = List_competition.objects.create(pk_list_competition='comp_1',
                                                            nom='Competition 1')
        lieu_competition = Lieu_des_competions.objects.create(pk_lieu='lieu_1', Nom='Lieu 1',
                                                               Ville='Ville 1', Capacite=100,
                                                               Discipline=list_competition)
        date_competition = Dates_Competions.objects.create(pk_date_competition='date_1',
                                                           date_debut='2024-08-01',
                                                           date_fin='2024-08-11',
                                                           pk_list_competition=list_competition,
                                                           pk_lieu=lieu_competition)

        # Créer une instance de Competitions avec les instances créées ci-dessus
        self.competition = Competitions.objects.create(pk_typ_competition='competition_1',
                                                       Nom='Competition 1',
                                                       pk_list_competition=list_competition,
                                                       pk_date_competition=date_competition,
                                                       pk_lieu=lieu_competition)

    def test_billet_creation(self):
        # Création d'un billet associé à la compétition
        billet = Billet.objects.create(pk_typ_competition=self.competition,
                                        ClefUtilisateur=123,
                                        Cledebilletelectroniquesecurisee='unique_key',  # Valeur pour le champ Cledebilletelectroniquesecurisee
                                        date_dachat=timezone.now(),
                                        date_valide=timezone.now())

        # Vérifier si le billet a été créé avec succès
        self.assertIsNotNone(billet)
        self.assertEqual(billet.pk_typ_competition, self.competition)
        self.assertFalse(billet.est_validee)

    def test_billet_update(self):
        # Créer un billet
        billet = Billet.objects.create(Cledebilletelectroniquesecurisee='cle_test',
                                       ClefUtilisateur='user_key',
                                       pk_typ_competition=self.competition,
                                       date_dachat=timezone.now(),
                                       date_valide=timezone.now())

        # Effectuer la mise à jour du billet
        billet.ClefUtilisateur = 'Bouramanew_user_key'
        billet.save()

        # Récupérer le billet mis à jour
        updated_billet = Billet.objects.get(ClefUtilisateur='Bouramanew_user_key')


        # Vérifier que la mise à jour a été effectuée correctement
        self.assertEqual(updated_billet.ClefUtilisateur, 'Bouramanew_user_key')

    def test_billet_deletion(self):
        # Créer un billet
        billet = Billet.objects.create(Cledebilletelectroniquesecurisee='cle_test',
                                        ClefUtilisateur='user_key',
                                        pk_typ_competition=self.competition,
                                        date_dachat=timezone.now(),
                                        date_valide=timezone.now())

        # Vérifier que le billet existe
        billet_exists = Billet.objects.filter(Cledebilletelectroniquesecurisee='cle_test').exists()
        print("Billet exists before deletion:", billet_exists)
        self.assertFalse(billet_exists)

        # Supprimer le billet
        billet.delete()

        # Vérifier que le billet n'existe plus
        billet_exists_after_deletion = Billet.objects.filter(Cledebilletelectroniquesecurisee='cle_test').exists()
        print("Billet exists after deletion:", billet_exists_after_deletion)
        self.assertFalse(billet_exists_after_deletion)



class CommandeCRUDTestCase(TestCase):
    """test Commande
    """
    def setUp(self):
        # Créer des instances nécessaires pour les tests
        self.user = get_user_model().objects.create_user(username='testuser', 
                                                         email='test@example.com', password='password')
        self.list_competition = List_competition.objects.create(pk_list_competition='Football',
                                                                 nom='Football')
        self.lieu_des_competions = Lieu_des_competions.objects.create(pk_lieu='Paris_Stade_10000_Football',
                                                                       Nom='Stade de Paris', Ville='Paris',
                                                                       Capacite=10000,
                                                                       Discipline=self.list_competition)
        self.dates_competions = Dates_Competions.objects.create(pk_date_competition='Football_Paris_Stade_2024-08-01_2024-08-11',
                                                                 date_debut=timezone.now(), 
                                                                 date_fin=timezone.now(), 
                                                                 pk_list_competition=self.list_competition,
                                                                 pk_lieu=self.lieu_des_competions, 
                                                                 Remises_de_medailles='Some medals')
        self.competition = Competitions.objects.create(Nom='Test Competition', pk_list_competition=self.list_competition,
                                                        pk_date_competition=self.dates_competions,
                                                          pk_lieu=self.lieu_des_competions)
        self.type  = Types.objects.create(type = 'One')

        self.offre = Offre.objects.create( 
                                         type = self.type, 
                                          nombre_personnes=1, 
                                          prix=10.0, 
                                          competition=self.competition)
        self.billet = Billet.objects.create(pk_typ_competition=self.competition,
                                            ClefUtilisateur=123,
                                            Cledebilletelectroniquesecurisee=456,
                                            date_dachat =timezone.now() ,
                                            date_valide = self.dates_competions.date_debut)
        
    def test_commande_creation(self):
        # Création d'une commande
        commande = Commande.objects.create(
            quantite=1,
            MontantTotal=10.0,
            pk_Offre=self.offre,
            pk_Utilisateur=self.user,
            pk_Billet=self.billet,
            est_validee=False
        )
        
        # Vérification de la création réussie
        self.assertIsNotNone(commande.pk_Commande)
        self.assertEqual(commande.pk_Offre, self.offre)
        self.assertEqual(commande.pk_Utilisateur, self.user)
        self.assertFalse(commande.est_validee)

    def test_commande_update(self):
        # Création d'une commande
        commande = Commande.objects.create(quantite=1,
                                           MontantTotal=10.0, 
                                           pk_Offre=self.offre, 
                                           pk_Utilisateur=self.user,
                                           pk_Billet=self.billet,
                                           est_validee=False)

        # Mise à jour de la commande
        commande.quantite = 2
        commande.save()

        # Récupération de la commande mise à jour depuis la base de données
        updated_commande = Commande.objects.get(pk_Commande=commande.pk_Commande)

        # Vérification de la mise à jour
        self.assertEqual(updated_commande.quantite, 2)

    def test_commande_delete(self):
        # Création d'une commande
        commande = Commande.objects.create(quantite=1,
                                            MontantTotal=10.0,
                                            pk_Offre=self.offre,
                                            pk_Utilisateur=self.user,
                                            pk_Billet=self.billet,
                                            est_validee=False)

        # Vérification que la commande existe
        commande_exists = Commande.objects.filter(pk_Commande=commande.pk_Commande).exists()
        self.assertTrue(commande_exists)

        # Suppression de la commande
        commande.delete()

        # Vérification que la commande n'existe plus
        commande_exists_after_deletion = Commande.objects.filter(pk_Commande=commande.pk_Commande).exists()
        self.assertFalse(commande_exists_after_deletion)

def test_ajouter_au_panier(self):
        # Simuler une requête POST pour ajouter une offre au panier
        response = self.client.post('/ajouter_au_panier/', {
            'offre_id': [self.offre.pk],
            'quantite_{}'.format(self.offre.pk): 2,
            'date_debut_{}'.format(self.offre.pk): '2024-08-01'
        })

        # Vérifier la redirection et la création de la commande
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/voir_panier/')
        self.assertEqual(Commande.objects.count(), 2)  

class VoirPanierTestCase(TestCase):
    """test Voir panier
    """
    def setUp(self):
        # Créer un utilisateur
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Connecter l'utilisateur
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        # Créer quelques instances de compétition et d'offre
        self.list_competition = List_competition.objects.create(pk_list_competition='comp_1',
                                                                nom='Compétition 1')
        self.lieu_competition = Lieu_des_competions.objects.create(pk_lieu='lieu_1',
                                                                   Nom='Lieu 1',
                                                                   Ville='Ville 1', 
                                                                   Capacite=100,
                                                                   Discipline=self.list_competition)
        self.date_competition = Dates_Competions.objects.create(pk_date_competition='date_1', 
                                                                date_debut='2024-08-01',
                                                                date_fin='2024-08-11',
                                                                pk_list_competition=self.list_competition,
                                                                pk_lieu=self.lieu_competition)

        self.competition = Competitions.objects.create(Nom=' wushu',
                                                       pk_list_competition=self.list_competition,
                                                       pk_date_competition=self.date_competition,
                                                       pk_lieu=self.lieu_competition)
        self.type = Types.objects.create(type ='One')
        self.offre = Offre.objects.create(
                                           type= self.type,
                                           nombre_personnes=1,
                                           prix=10.0,
                                           competition=self.competition
                                          )

        # Créer une commande pour l'utilisateur
        self.commande = Commande.objects.create(quantite=1,
                                                pk_Offre=self.offre,
                                                MontantTotal=10.0,
                                                pk_Utilisateur=self.user)

    def test_voir_panier(self):
        # Envoyer une requête GET à la vue voir_panier
        response = self.client.get(reverse('voir_panier'))

        # Vérifier que la réponse est réussie (code 200)
        self.assertEqual(response.status_code, 200)

        # Vérifier que la commande de l'utilisateur est présente dans le contexte de la réponse
        self.assertIn(self.commande, response.context['commandes'])



class ModifierCommandeTestCase(TestCase):
    """Test Modifier Commande
    """
    def setUp(self):
        # Créer une commande et une offre pour le test
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.list_competition = List_competition.objects.create(pk_list_competition='comp_1',
                                                                nom='Compétition 1')
        self.lieu_competition = Lieu_des_competions.objects.create(pk_lieu='lieu_1',
                                                                   Nom='Lieu 1', 
                                                                   Ville='Ville 1',
                                                                   Capacite=100,
                                                                   Discipline=self.list_competition)
        self.date_competition = Dates_Competions.objects.create(pk_date_competition='date_1',
                                                                date_debut='2024-08-01',
                                                                date_fin='2024-08-11',
                                                                pk_list_competition=self.list_competition,
                                                                pk_lieu=self.lieu_competition)

        self.competition = Competitions.objects.create(Nom='Test Competition',
                                                       pk_list_competition=self.list_competition, 
                                                       pk_date_competition=self.date_competition, 
                                                       pk_lieu=self.lieu_competition)
        self.type =Types.objects.create(type = 'One')
        self.offre = Offre.objects.create(type= self.type,
                                          nombre_personnes=1,
                                          prix=10.0,
                                          competition=self.competition)

        # Créer une commande pour l'utilisateur
        self.commande = Commande.objects.create(quantite=1, 
                                                MontantTotal=10.0,
                                                pk_Offre=self.offre,
                                                pk_Utilisateur=self.user)

        # Créer un client et se connecter en tant qu'utilisateur pour simuler une requête
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_modifier_commande(self):
        # Définir l'URL pour la vue modifier_commande avec l'ID de commande comme paramètre
        url = reverse('modifier_commande', kwargs={'commande_id': self.commande.pk})

        # Envoyer une requête POST pour modifier la commande
        response = self.client.post(url, {'offre_id': self.offre.pk, 'quantite': 2})

        # Vérifier que la réponse redirige vers la vue voir_panier
        self.assertRedirects(response, reverse('voir_panier'))

        # Vérifier que la commande a été mise à jour avec les nouvelles données
        commande_modifiee = Commande.objects.get(pk=self.commande.pk)
        self.assertEqual(commande_modifiee.pk_Offre, self.offre)
        self.assertEqual(commande_modifiee.quantite, 2)
        self.assertEqual(commande_modifiee.MontantTotal, 20.0)

class SupprimerCommandeTestCase(TestCase):
    """test Supprimer Commande
    """
    def setUp(self):
        # Créer un utilisateur
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Créer une commande pour l'utilisateur
        self.list_competition = List_competition.objects.create(pk_list_competition='comp_1',
                                                                nom='judo ')
        self.lieu_competition = Lieu_des_competions.objects.create(pk_lieu='lieu_1',
                                                                   Nom='Lieu 1',
                                                                   Ville='Ville 1',
                                                                   Capacite=100,
                                                                   Discipline=self.list_competition)
        self.date_competition = Dates_Competions.objects.create(pk_date_competition='date_1',
                                                                date_debut='2024-08-01', 
                                                                date_fin='2024-08-11',
                                                                pk_list_competition=self.list_competition,
                                                                pk_lieu=self.lieu_competition)

        self.competition = Competitions.objects.create(Nom='Test Competition', 
                                                       pk_list_competition=self.list_competition, 
                                                       pk_date_competition=self.date_competition, 
                                                       pk_lieu=self.lieu_competition)
        self.type =Types.objects.create(type ='fammille')
        self.offre = Offre.objects.create(type= self.type,
                                         nombre_personnes= 4,
                                         prix=40.0, 
                                         competition=self.competition)
        self.commande = Commande.objects.create(
                                               pk_Offre=self.offre,
                                               quantite=1,
                                                MontantTotal=10.0, 
                                                pk_Utilisateur=self.user)

        # Créer une commande pour l'utilisateur
        self.commande = Commande.objects.create(quantite=1, 
                                                MontantTotal=40.0,
                                                pk_Offre=self.offre,
                                                pk_Utilisateur=self.user)

        # Se connecter en tant qu'utilisateur pour simuler une requête
        self.client.login(username='testuser', password='testpassword')

    def test_supprimer_commande(self):
        # Définir l'URL pour la vue supprimer_commande avec l'ID de commande comme paramètre
        url = reverse('supprimer_commande', kwargs={'commande_id': self.commande.pk})
        
        # Envoyer une requête POST pour supprimer la commande
        response = self.client.post(url)
        
        # Vérifier que la réponse redirige vers la vue voir_panier
        self.assertRedirects(response, reverse('voir_panier'))
        
        # Vérifier que la commande a été supprimée de la base de données
        self.assertFalse(Commande.objects.filter(pk=self.commande.pk).exists())
        
        

class DetailsBilletTestCase(TestCase):
    """test Details Billet
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser',
                                                        email='test@example.com',
                                                        password='password')
        self.list_competition = List_competition.objects.create(pk_list_competition='Football', 
                                                                nom='Football')
        self.lieu_des_competions = Lieu_des_competions.objects.create(pk_lieu='Paris_Stade_10000_Football',
                                                                      Nom='Stade de Paris',
                                                                      Ville='Paris',
                                                                      Capacite=10000,
                                                                      Discipline=self.list_competition)
        self.dates_competions = Dates_Competions.objects.create(pk_date_competition='Football_Paris_Stade_2024-08-01_2024-08-11',
                                                                date_debut=timezone.now(), 
                                                                date_fin=timezone.now(),
                                                                pk_list_competition=self.list_competition, 
                                                                pk_lieu=self.lieu_des_competions, 
                                                                Remises_de_medailles='Some medals')
        self.competition = Competitions.objects.create(Nom='Test Competition',
                                                       pk_list_competition=self.list_competition,
                                                        pk_date_competition=self.dates_competions,
                                                          pk_lieu=self.lieu_des_competions)
        self.type = Types.objects.create(type ='one')
        self.offre = Offre.objects.create(type= self.type,
                                          nombre_personnes=1, prix=10.0,
                                          competition=self.competition)
        self.billet = Billet.objects.create(pk_typ_competition=self.competition,
                                            ClefUtilisateur=123,
                                            Cledebilletelectroniquesecurisee=456,
                                            date_dachat =timezone.now() ,
                                            date_valide = self.dates_competions.date_debut)
        self.commande = Commande.objects.create(quantite=2,
                                                MontantTotal=50.0, 
                                                pk_Offre=self.offre,
                                                pk_Utilisateur=self.user)
        self.billet.commande_set.add(self.commande)
    
    def test_details_billet(self):
        # Définir l'URL pour la vue details_billet avec l'ID de billet comme paramètre
        url = reverse('details_billet', kwargs={'billet_id': self.billet.pk})

        # Envoyer une requête GET pour obtenir les détails du billet
        response = self.client.get(url)

        # Vérifier que la réponse a un statut HTTP 200 (OK)
        self.assertEqual(response.status_code, 200)

       

class TestUrls(TestCase):
    """test url
    """
    def setUp(self):
        # Créer une instance de RequestFactory
        self.factory = RequestFactory()

    def test_home_url(self):
        # Créer une requête GET pour l'URL de la vue home
        request = self.factory.get(reverse('home'))

        # Appeler la fonction resolve avec l'URL pour obtenir la vue correspondante
        resolver = resolve('/')

        # Vérifier que la vue correspond à la fonction home
        self.assertEqual(resolver.func, home)

    def test_choisir_ticket_url(self):
        # Créer une requête GET pour l'URL de la vue choisir_ticket
        request = self.factory.get(reverse('choisir_ticket'))

        # Appeler la fonction resolve avec l'URL pour obtenir la vue correspondante
        resolver = resolve('/choisir_ticket/')

        # Vérifier que la vue correspond à la fonction choisir_ticket
        self.assertEqual(resolver.func, choisir_ticket)

    def test_ajouter_au_panier_url(self):
        # Créer une requête GET pour l'URL de la vue ajouter_au_panier
        request = self.factory.get(reverse('ajouter_au_panier'))
        

class ChoixTicketTestCase(TestCase):
    """test Choisir le ticket
    """
    def setUp(self):
                
        User.objects.all().delete()

        self.list_competition = List_competition.objects.create(pk_list_competition='comp_1', nom='Compétition 1')
        self.lieu_competition = Lieu_des_competions.objects.create(pk_lieu='lieu_1', Nom='Lieu 1', Ville='Ville 1', Capacite=100, Discipline=self.list_competition)
        self.date_competition = Dates_Competions.objects.create(pk_date_competition='date_1', date_debut='2024-08-01', date_fin='2024-08-11', pk_list_competition=self.list_competition, pk_lieu=self.lieu_competition)
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.competition = Competitions.objects.create(Nom='Test Competition', pk_list_competition=self.list_competition, pk_date_competition=self.date_competition, pk_lieu=self.lieu_competition)
        self.type = Types.objects.create(type='Duo')
        self.offre = Offre.objects.create(type=self.type, nombre_personnes=2, prix=20.0, competition=self.competition)
    def test_inscription_view(self):
        # Tester la vue d'inscription avec une requête POST valide
        response = self.client.post(reverse('inscription'),
                                     {'username': 'newuser', 
                                      'password1': 'newpassword',
                                      'password2': 'newpassword'})
        # Redirection après une inscription réussie
        self.assertEqual(response.status_code, 200)  

    def test_connexion_view(self):
        # Tester la vue de connexion avec une requête POST valide
        response = self.client.post(reverse('connexion'), 
                                    {'username': 'testuser',
                                     'password': 'testpassword'})
        # Redirection après une connexion réussie
        self.assertEqual(response.status_code, 302)  

    def test_deconnexion_view(self):
        # Se connecter d'abord
        self.client.login(username='testuser',
                          password='testpassword')

        # Tester la vue de déconnexion
        response = self.client.get(reverse('deconnexion'))
        self.assertEqual(response.status_code, 302)  # Redirection après une déconnexion réussie

    def test_ventes_par_offre_view(self):
        # Créer un utilisateur administrateur pour accéder à la vue admin
        admin_user = User.objects.create_superuser(username='admin',
                                                   email='admin@example.com',
                                                    password='adminpassword')
        self.client.login(username='admin', password='adminpassword')

        # Tester la vue ventes_par_offre
        response = self.client.get(reverse('ventes_par_offre'))
        self.assertEqual(response.status_code, 200)

    def test_choisir_ticket_get(self):
        url = reverse('choisir_ticket')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'choisir_ticket.html')

    def test_choisir_ticket_post(self):
        competition_id = self.competition.pk  # Utiliser la bonne clé primaire de la compétition
        response = self.client.post(reverse('choisir_ticket'), {'competition': competition_id})
        self.assertEqual(response.status_code, 200)

    def test_ajouter_au_panier_post(self):
        """test ajouter au panier
        """
       
        self.list_competition = List_competition.objects.create(pk_list_competition='escrime',
                                                                nom='escrime')
        self.lieu_competition = Lieu_des_competions.objects.create(pk_lieu='paris_escrime',
                                                                   Nom='escrime club', 
                                                                   Ville='Paris',
                                                                   Capacite=100,
                                                                   Discipline=self.list_competition)
        self.date_competition = Dates_Competions.objects.create(pk_date_competition='date_3',
                                                                date_debut='2024-09-02',
                                                                date_fin='2024-09-12',
                                                                pk_list_competition=self.list_competition,
                                                                pk_lieu=self.lieu_competition)
       
        self.competition = Competitions.objects.create(Nom='escrime',
                                                       pk_list_competition=self.list_competition, 
                                                       pk_date_competition=self.date_competition, 
                                                       pk_lieu=self.lieu_competition)
        self.type =Types.objects.create(type ='groupe')
        self.offre = Offre.objects.create(type= self.type,
                                          nombre_personnes=1,
                                          prix=10.0,
                                          competition=self.competition)

        # Créer une commande pour l'utilisateur
        self.commande = Commande.objects.create(quantite=1, MontantTotal=10.0,
                                                pk_Offre=self.offre,
                                                pk_Utilisateur=self.user,
                                                est_validee=True)
        self.billet = Billet.objects.create(pk_typ_competition=self.competition,
                                            ClefUtilisateur=123,
                                            Cledebilletelectroniquesecurisee=456,
                                            date_dachat =timezone.now() ,
                                            date_valide = timezone.now())
        # Créer un client et se connecter en tant qu'utilisateur pour simuler une requête
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        url = reverse('ajouter_au_panier')
        response = self.client.post(url, {'offre_id': self.offre.pk_Offre, 'quantite_' + str(self.offre.pk_Offre): 1})
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Commande.objects.count(), 1)
        self.assertEqual(Billet.objects.count(), 2)
        commande = Commande.objects.first()
        self.assertEqual(commande.quantite, 1)
        self.assertEqual(commande.MontantTotal, 10.0)
        self.assertEqual(commande.pk_Offre, self.offre)
        self.assertEqual(commande.pk_Utilisateur, self.user)
        self.assertTrue(commande.est_validee) 
        self.assertAlmostEqual(commande.pk_date, timezone.now(), delta=timezone.timedelta(seconds=10)) 

    def test_voir_panier(self):
        # Créer une instance de RequestFactory
            request_factory = RequestFactory()

        # Créer une requête GET pour la vue voir_panier
            request = request_factory.get(reverse('voir_panier'))

        # Ajouter l'utilisateur à la requête pour simuler une session utilisateur
            request.user = self.user

        # Ajouter un message à la session (simulant un message flash)
            setattr(request, 'session', 'session')
            messages = FallbackStorage(request)
            setattr(request, '_messages', messages)

        # Appeler la vue voir_panier en utilisant la requête
            response = voir_panier(request)

        # Vérifier que la réponse renvoie un code 200 (succès)
            self.assertEqual(response.status_code, 200) 


class TestViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.list_competition = List_competition.objects.create(pk_list_competition='escrime',
                                                                nom='escrime')
        self.lieu_competition = Lieu_des_competions.objects.create(pk_lieu='paris_escrime',
                                                                   Nom='escrime club', 
                                                                   Ville='Paris',
                                                                   Capacite=100,
                                                                   Discipline=self.list_competition)
        self.date_competition = Dates_Competions.objects.create(pk_date_competition='date_3',
                                                                date_debut='2024-09-02',
                                                                date_fin='2024-09-12',
                                                                pk_list_competition=self.list_competition,
                                                                pk_lieu=self.lieu_competition)
        
        image_file = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')

        self.competition = Competitions.objects.create(pk_typ_competition ='escrime',
                                                       Nom='escrime',
                                                        image=image_file,
                                                       pk_list_competition=self.list_competition, 
                                                       pk_date_competition=self.date_competition, 
                                                       pk_lieu=self.lieu_competition)   
        self.type = Types.objects.create(type='Test Type')
        self.offre = Offre.objects.create(type= self.type,
                                          nombre_personnes=1,
                                          prix=10.0,
                                          competition=self.competition)
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
       

    def test_home_view(self):
        request = self.factory.get('/')
        response = home(request)
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'home.html')

    def test_choisir_ticket_view_get(self):
        request = self.factory.get(reverse('choisir_ticket'))
        response = choisir_ticket(request)
        self.assertEqual(response.status_code, 200)

    def test_choisir_ticket_with_competition_only(self):
        response = self.client.get(reverse('choisir_ticket'), {'competition': self.competition.pk_typ_competition})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'choisir_ticket.html')
        self.assertIn('page_objs', response.context)
        self.assertIn('competitions', response.context)

    def test_choisir_ticket_with_competition_and_type(self):
        response = self.client.get(reverse('choisir_ticket'), {'competition': self.competition.pk_typ_competition, 'type': self.type.type})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'choisir_ticket.html')
        self.assertIn('page_objs', response.context)
        self.assertEqual(len(response.context['page_objs']), 1)
        self.assertEqual(response.context['page_objs'][0], self.offre)
        self.assertIn('competitions', response.context)

    def test_choisir_ticket_without_competition(self):
        response = self.client.get(reverse('choisir_ticket'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'choisir_ticket.html')
        self.assertNotIn('page_objs', response.context)
        self.assertIn('competitions', response.context)
        self.assertEqual(len(response.context['competitions']), 1)
        self.assertEqual(response.context['competitions'][0], self.competition)
   
    
    def test_ajouter_au_panier_success(self):
        data = {
            'offre_id': [self.offre.pk_Offre],
            'quantite_{}'.format(self.offre.pk_Offre): 2,
            'date_debut_{}'.format(self.offre.pk_Offre): '2024-05-25',
        }
        response = self.client.post(reverse('ajouter_au_panier'), data)
        self.assertRedirects(response, reverse('voir_panier'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Les offres ont été ajoutées au panier.")
        
        commandes = Commande.objects.filter(pk_Utilisateur=self.user)
        self.assertEqual(commandes.count(), 1)

    def test_ajouter_au_panier_invalid_quantity(self):
        data = {
            'offre_id': [self.offre.pk_Offre],
            'quantite_{}'.format(self.offre.pk_Offre): 0,
            'date_debut_{}'.format(self.offre.pk_Offre): '2024-05-25',
        }
        response = self.client.post(reverse('ajouter_au_panier'), data)
        self.assertRedirects(response, reverse('choisir_ticket'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Veuillez sélectionner au moins une offre et spécifier une quantité valide.")
        
        commandes = Commande.objects.filter(pk_Utilisateur=self.user)
        self.assertEqual(commandes.count(), 0)

    def test_ajouter_au_panier_offer_does_not_exist(self):
        data = {
            'offre_id': [999],  
            'quantite_999': 1,
            'date_debut_999': '2024-05-25',
        }
        response = self.client.post(reverse('ajouter_au_panier'), data)
        self.assertRedirects(response, reverse('choisir_ticket'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "L'offre avec l'ID 999 n'existe pas.")
        
        commandes = Commande.objects.filter(pk_Utilisateur=self.user)
        self.assertEqual(commandes.count(), 0)

    def test_ajouter_au_panier_missing_start_date(self):
        data = {
            'offre_id': [self.offre.pk_Offre],
            'quantite_{}'.format(self.offre.pk_Offre): 1,
             'date_debut_{}'.format(self.offre.pk_Offre): ' ',

        }
        response = self.client.post(reverse('ajouter_au_panier'), data)
        self.assertRedirects(response, reverse('choisir_ticket'))
        
        commandes = Commande.objects.filter(pk_Utilisateur=self.user)
        self.assertEqual(commandes.count(), 0)


class PayerCommandeViewTests(TestCase):
    """teste payer commande
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='12345')
        self.client.login(username='user', password='12345')
        
        self.list_competition = List_competition.objects.create(pk_list_competition='escrime',
                                                                nom='escrime')
        self.lieu_competition = Lieu_des_competions.objects.create(pk_lieu='paris_escrime',
                                                                   Nom='escrime club', 
                                                                   Ville='Paris',
                                                                   Capacite=100,
                                                                   Discipline=self.list_competition)
        self.date_competition = Dates_Competions.objects.create(pk_date_competition='date_3',
                                                                date_debut='2024-09-02',
                                                                date_fin='2024-09-12',
                                                                pk_list_competition=self.list_competition,
                                                                pk_lieu=self.lieu_competition)
        
        image_file = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')

        self.competition = Competitions.objects.create(pk_typ_competition ='escrime',
                                                       Nom='escrime',
                                                        image=image_file,
                                                       pk_list_competition=self.list_competition, 
                                                       pk_date_competition=self.date_competition, 
                                                       pk_lieu=self.lieu_competition)   
        self.type = Types.objects.create(type='Test Type')
        self.offre = Offre.objects.create(type= self.type,
                                          nombre_personnes=1,
                                          prix=10.0,
                                          competition=self.competition)
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.commande = Commande.objects.create(quantite=1, MontantTotal=10.0,
                                                pk_Offre=self.offre,
                                                pk_Utilisateur=self.user,
                                                est_validee=False)
        
        self.billet = Billet.objects.create(pk_typ_competition=self.competition,
                                            ClefUtilisateur=123,
                                            Cledebilletelectroniquesecurisee=456,
                                            date_dachat =timezone.now() ,
                                            date_valide = timezone.now())
        

    def test_payer_commande_success(self):
         response = self.client.post(reverse('payer_commande', args=[self.commande.pk_Commande]))
        #  self.assertRedirects(response, reverse('details_billet', args=[self.billet.pk_Billet]))  # Correction ici
    
         self.commande.refresh_from_db()
         self.assertTrue(self.commande.est_validee)
    
        #  self.billet.refresh_from_db()
        #  self.assertTrue(self.billet.est_validee)


    def test_payer_commande_already_validated(self):
        self.commande.est_validee = True
        self.commande.save()
        
        response = self.client.post(reverse('payer_commande', args=[self.commande.pk_Commande]))
        self.assertRedirects(response, reverse('voir_panier'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "La commande n'existe pas ou a déjà été validée.")

    def test_payer_commande_nonexistent(self):
        response = self.client.post(reverse('payer_commande', args=[999]))  # Commande ID that does not exist
        self.assertRedirects(response, reverse('voir_panier'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "La commande n'existe pas ou a déjà été validée.")

    def test_payer_commande_get(self):
        response = self.client.get(reverse('payer_commande', args=[self.commande.pk_Commande]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payer_commande.html')
        self.assertIn('commande_id', response.context)
        self.assertIn('montant_total', response.context)
        # self.assertEqual(response.context['montant_total'], self.commande.MontantTotal)

    
class ModifierCommandeTestCase(TestCase):
    """test modification
    """
    def setUp(self):
        # Créer des objets Commande et Offre pour les tests
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='12345')
        self.client.login(username='user', password='12345')
        
        self.list_competition = List_competition.objects.create(pk_list_competition='escrime',
                                                                nom='escrime')
        self.lieu_competition = Lieu_des_competions.objects.create(pk_lieu='paris_escrime',
                                                                   Nom='escrime club', 
                                                                   Ville='Paris',
                                                                   Capacite=100,
                                                                   Discipline=self.list_competition)
        self.date_competition = Dates_Competions.objects.create(pk_date_competition='date_3',
                                                                date_debut='2024-09-02',
                                                                date_fin='2024-09-12',
                                                                pk_list_competition=self.list_competition,
                                                                pk_lieu=self.lieu_competition)
        
        image_file = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')

        self.competition = Competitions.objects.create(pk_typ_competition ='escrime',
                                                       Nom='escrime',
                                                        image=image_file,
                                                       pk_list_competition=self.list_competition, 
                                                       pk_date_competition=self.date_competition, 
                                                       pk_lieu=self.lieu_competition)   
        self.type = Types.objects.create(type='Test Type')
        self.offre = Offre.objects.create(type= self.type,
                                          nombre_personnes=1,
                                          prix=10.0,
                                          competition=self.competition)
        self.user = User.objects.create_user(username='amina', password='12345455')
        self.client.login(username='amina', password='12345455')
        self.commande = Commande.objects.create(quantite=1, MontantTotal=10.0,
                                                pk_Offre=self.offre,
                                                pk_Utilisateur=self.user,
                                                est_validee=False)
        
        self.billet = Billet.objects.create(pk_typ_competition=self.competition,
                                            ClefUtilisateur=123,
                                            Cledebilletelectroniquesecurisee=456,
                                            date_dachat =timezone.now() ,
                                            date_valide = timezone.now())
        

    def test_modifier_commande_post(self):
        # Simuler une requête POST avec des données de modification de commande
        data = {
            'offre_id': self.offre.pk_Offre,
            'quantite': 2,
        }
        response = self.client.post(reverse('modifier_commande', args=[self.commande.pk_Commande]), data)
        
        # Vérifier que la réponse redirige vers 'voir_panier'
        self.assertRedirects(response, reverse('voir_panier'))

        # Actualiser l'objet commande depuis la base de données
        self.commande.refresh_from_db()

        # Vérifier que la commande a été mise à jour avec les nouvelles données
        self.assertEqual(self.commande.pk_Offre, self.offre)
        self.assertEqual(self.commande.quantite, 2)
        self.assertEqual(self.commande.MontantTotal, 20)

    # Ajouter d'autres tests unitaires pour les différentes branches de votre vue

    def test_modifier_commande_get(self):
        # Simuler une requête GET à la vue
        response = self.client.get(reverse('modifier_commande', args=[self.commande.pk_Commande]))

        # Vérifier que la réponse est un succès (code 200)
        self.assertEqual(response.status_code, 200)

class InscriptionTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_inscription_post(self):
        # Créer des données simulées pour le formulaire d'inscription
        data = {
            'username': 'testuser',
            'last_name': 'Doe',
            'first_name': 'John',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'accept_conditions': True,
            # Ajoutez d'autres champs requis par votre formulaire ici
        }

        # Envoyer une requête POST avec les données simulées
        response = self.client.post(reverse('inscription'), data)

        # Vérifier que l'utilisateur est créé dans la base de données
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

        # Vérifier que l'utilisateur est connecté
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_inscription_get(self):
        # Envoyer une requête GET à la vue d'inscription
        response = self.client.get(reverse('inscription'))

        # Vérifier que la réponse est un succès (code 200)
        self.assertEqual(response.status_code, 200)

        # Vérifier que le formulaire est présent dans le contexte
        self.assertIn('form', response.context)

        # Vérifier que tous les champs requis sont présents dans le formulaire
        form = response.context['form']
        self.assertIn('username', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('first_name', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('phone_number', form.fields)
        self.assertIn('password1', form.fields)
        self.assertIn('password2', form.fields)
        self.assertIn('accept_conditions', form.fields)




@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', first_name='Test', last_name='User', password='12345')

@pytest.fixture
def billet(db):
    return Billet.objects.create(pk_Billet=1, ClefUtilisateur='clef_user', Cledebilletelectroniquesecurisee='clef_billet')

@pytest.fixture
def commande(db, billet, user):
    return Commande.objects.create(pk_Billet=billet, pk_Utilisateur=user, est_validee=True)

@patch('my_app_jo.views.qrcode.QRCode')  # Remplacez par le chemin correct vers votre vue
def test_mes_billets(mock_qrcode, client, billet, commande):
    # Mocking QRCode generation
    mock_qr_instance = mock_qrcode.return_value
    mock_img_instance = mock_qr_instance.make_image.return_value
    mock_img_instance.save = lambda buffer, format: buffer.write(b'fake image data')

    response = client.get(reverse('mes_billets'))  

    assert response.status_code == 200
    assert 'billets_with_qr' in response.context
    billets_with_qr = response.context['billets_with_qr']
    
    assert len(billets_with_qr) == 1
    assert billets_with_qr[0]['billet'] == billet
    assert billets_with_qr[0]['commande'] == commande
    assert billets_with_qr[0]['qr_image'] == base64.b64encode(b'fake image data').decode() 


class ProfileViewTest(TestCase):
    def setUp(self):
        # Crée un utilisateur de test
        self.user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            password='12345'
        )
        # Instancie le client de test
        self.client = Client()

    def test_profile_view(self):
        # Force la connexion de l'utilisateur
        self.client.force_login(self.user)

        # Fait une requête GET vers la vue 'profile'
        response = self.client.get(reverse('profile'))

        # Vérifie que le statut de la réponse est 200
        self.assertEqual(response.status_code, 200)
        # Vérifie que le contexte contient l'utilisateur
        self.assertIn('user', response.context)
        # Vérifie que l'utilisateur dans le contexte est le bon utilisateur
        self.assertEqual(response.context['user'], self.user)
        # Vérifie que le template utilisé est 'profile.html'
        self.assertTemplateUsed(response, 'profile.html')



class ModifierProfileViewTest(TestCase):
    def setUp(self):
        # Crée un utilisateur de test
        self.user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            password='12345'
        )
        # Crée une instance de RequestFactory
        self.factory = RequestFactory()

    def test_modifier_profile_get(self):
        # Crée une requête GET
        request = self.factory.get(reverse('modifier_profile'))
        # Assigne l'utilisateur à la requête
        request.user = self.user

        # Appelle la vue
        response = modifier_profile(request)

        # Vérifie que le statut de la réponse est 200
        self.assertEqual(response.status_code, 200)

    
class OffresUserViewTest(TestCase):
    def setUp(self):
        # Crée quelques offres de test
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='12345')
        self.client.login(username='user', password='12345')
        
        self.list_competition = List_competition.objects.create(pk_list_competition='escrime',
                                                                nom='escrime')
        self.lieu_competition = Lieu_des_competions.objects.create(pk_lieu='paris_escrime',
                                                                   Nom='escrime club', 
                                                                   Ville='Paris',
                                                                   Capacite=100,
                                                                   Discipline=self.list_competition)
        self.date_competition = Dates_Competions.objects.create(pk_date_competition='date_3',
                                                                date_debut='2024-09-02',
                                                                date_fin='2024-09-12',
                                                                pk_list_competition=self.list_competition,
                                                                pk_lieu=self.lieu_competition)
        
        image_file = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')

        self.competition = Competitions.objects.create(pk_typ_competition ='escrime',
                                                       Nom='escrime',
                                                        image=image_file,
                                                       pk_list_competition=self.list_competition, 
                                                       pk_date_competition=self.date_competition, 
                                                       pk_lieu=self.lieu_competition)   
        self.type = Types.objects.create(type='Test Type')
        self.offre = Offre.objects.create(type= self.type,
                                          nombre_personnes=1,
                                          prix=10.0,
                                          competition=self.competition)
        # Crée une instance de RequestFactory
        self.factory = RequestFactory()

    def test_offresuser_get(self):
        # Crée une requête GET
        request = self.factory.get(reverse('offresuser'))  # Assurez-vous que le nom de l'URL est correct
        # Appelle la vue
        response = offresuser(request)

        # Vérifie que le statut de la réponse est 200
        self.assertEqual(response.status_code, 200)
       
     