from django.test import TestCase,Client
from django.test import TestCase, RequestFactory
from .models import Competitions ,Lieu_des_competions,List_competition,Dates_Competions,Offre,Commande,User,Billet
from datetime import datetime
from django.utils import timezone
from my_app_jo.views import choisir_ticket
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from .views import ajouter_au_panier

import string
import secrets

class ListCompetitionCRUDTestCase(TestCase):
    def setUp(self):
        # Créer une instance de List_competition pour les tests
        self.football_competition = List_competition.objects.create(pk_list_competition='Football', nom='Football')

    def test_create_list_competition(self):
        # Vérifier si l'instance de List_competition a été créée avec succès
        new_competition = List_competition.objects.create(pk_list_competition='Basketball', nom='Basketball')
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
    def setUp(self):
        # Créer une instance de List_competition pour les tests
        self.list_competition = List_competition.objects.create(pk_list_competition='Football', nom='Football')

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
    def setUp(self):
        # Créer des instances de List_competition et Lieu_des_competions pour les tests
        self.list_competition = List_competition.objects.create(pk_list_competition='Football', nom='Football')
        self.lieu_des_competions = Lieu_des_competions.objects.create(pk_lieu='Paris_Stade_10000_Football', Nom='Stade de Paris', Ville='Paris', Capacite=10000, Discipline=self.list_competition)

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

class OffreCRUDTestCase(TestCase):
    def setUp(self):
        # Création des instances 
        self.list_competition = List_competition.objects.create(pk_list_competition='Football', nom='Football')
        self.lieu_des_competions = Lieu_des_competions.objects.create(pk_lieu='Paris_Stade_10000_Football', Nom='Stade de Paris', Ville='Paris', Capacite=10000, Discipline=self.list_competition)
        self.dates_competions = Dates_Competions.objects.create(pk_date_competition='Football_Paris_Stade_2024-08-01_2024-08-11', date_debut=datetime(2024, 8, 1), date_fin=datetime(2024, 8, 11), pk_list_competition=self.list_competition, pk_lieu=self.lieu_des_competions, Remises_de_medailles='Some medals')
        self.competition = Competitions.objects.create(Nom='Test Competition', pk_list_competition=self.list_competition, pk_date_competition=self.dates_competions, pk_lieu=self.lieu_des_competions)

    def test_offre_CRUD(self):
        # Test de création
        new_offre = Offre.objects.create(
            type='One',
            nombre_personnes=1,
            prix=10.0,
            competition=self.competition
        )
        self.assertIsNotNone(new_offre.pk_Offre)

        # Test de lecture
        retrieved_offre = Offre.objects.get(pk_Offre=new_offre.pk_Offre)
        self.assertEqual(retrieved_offre.type, 'One')

        # Test de mise à jour
        retrieved_offre.type = 'Duo'
        retrieved_offre.save()

        # Récupérer à nouveau l'objet mis à jour
        updated_offre = Offre.objects.get(pk_Offre=new_offre.pk_Offre)
        self.assertEqual(updated_offre.type, 'Duo')

        # Test de suppression
        updated_offre.delete()
        with self.assertRaises(Offre.DoesNotExist):
            Offre.objects.get(pk_Offre=new_offre.pk_Offre)

class BilletCRUDTestCase(TestCase):

    def setUp(self):
        # Créer des instances nécessaires pour Competitions
        list_competition = List_competition.objects.create(pk_list_competition='comp_1', nom='Competition 1')
        lieu_competition = Lieu_des_competions.objects.create(pk_lieu='lieu_1', Nom='Lieu 1', Ville='Ville 1', Capacite=100, Discipline=list_competition)
        date_competition = Dates_Competions.objects.create(pk_date_competition='date_1', date_debut='2024-08-01', date_fin='2024-08-11', pk_list_competition=list_competition, pk_lieu=lieu_competition)

        # Créer une instance de Competitions avec les instances créées ci-dessus
        self.competition = Competitions.objects.create(pk_typ_competition='competition_1', Nom='Competition 1', pk_list_competition=list_competition, pk_date_competition=date_competition, pk_lieu=lieu_competition)

    def test_billet_creation(self):
        # Création d'un billet associé à la compétition
        billet = Billet.objects.create(pk_typ_competition=self.competition)
        
        # Vérifier si le billet a été créé avec succès
        self.assertIsNotNone(billet)
        self.assertEqual(billet.pk_typ_competition, self.competition)
        self.assertFalse(billet.est_validee)  
    def test_billet_update(self):
    # Créer un billet
        billet = Billet.objects.create(Cledebilletelectroniquesecurisee='cle_test', ClefUtilisateur='user_key', pk_typ_competition=self.competition)

    # Effectuer la mise à jour du billet
        billet.ClefUtilisateur = 'new_user_key'
        billet.save()
    
    # Récupérer le billet mis à jour
        updated_billet = Billet.objects.get(Cledebilletelectroniquesecurisee='cle_test')

    # Vérifier que la mise à jour a été effectuée correctement
        self.assertEqual(updated_billet.ClefUtilisateur, 'new_user_key')    
    def test_billet_deletion(self):
    # Créer un billet
        billet = Billet.objects.create(Cledebilletelectroniquesecurisee='cle_test', ClefUtilisateur='user_key', pk_typ_competition=self.competition)

    # Vérifier que le billet existe
        billet_exists = Billet.objects.filter(Cledebilletelectroniquesecurisee='cle_test').exists()
        self.assertTrue(billet_exists)

    # Supprimer le billet
        billet.delete()

    # Vérifier que le billet n'existe plus
        billet_exists_after_deletion = Billet.objects.filter(Cledebilletelectroniquesecurisee='cle_test').exists()
        self.assertFalse(billet_exists_after_deletion)    


class CommandeCRUDTestCase(TestCase):
    def setUp(self):
        # Créer des instances nécessaires pour les tests
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='password')
        self.list_competition = List_competition.objects.create(pk_list_competition='Football', nom='Football')
        self.lieu_des_competions = Lieu_des_competions.objects.create(pk_lieu='Paris_Stade_10000_Football', Nom='Stade de Paris', Ville='Paris', Capacite=10000, Discipline=self.list_competition)
        self.dates_competions = Dates_Competions.objects.create(pk_date_competition='Football_Paris_Stade_2024-08-01_2024-08-11', date_debut=timezone.now(), date_fin=timezone.now(), pk_list_competition=self.list_competition, pk_lieu=self.lieu_des_competions, Remises_de_medailles='Some medals')
        self.competition = Competitions.objects.create(Nom='Test Competition', pk_list_competition=self.list_competition, pk_date_competition=self.dates_competions, pk_lieu=self.lieu_des_competions)
        self.offre = Offre.objects.create(type='One', nombre_personnes=1, prix=10.0, competition=self.competition)
        self.billet = Billet.objects.create(pk_typ_competition=self.competition)
        
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
        commande = Commande.objects.create(quantite=1, MontantTotal=10.0, pk_Offre=self.offre, pk_Utilisateur=self.user, pk_Billet=self.billet, est_validee=False)

        # Mise à jour de la commande
        commande.quantite = 2
        commande.save()

        # Récupération de la commande mise à jour depuis la base de données
        updated_commande = Commande.objects.get(pk_Commande=commande.pk_Commande)

        # Vérification de la mise à jour
        self.assertEqual(updated_commande.quantite, 2)

    def test_commande_delete(self):
        # Création d'une commande
        commande = Commande.objects.create(quantite=1, MontantTotal=10.0, pk_Offre=self.offre, pk_Utilisateur=self.user, pk_Billet=self.billet, est_validee=False)

        # Vérification que la commande existe
        commande_exists = Commande.objects.filter(pk_Commande=commande.pk_Commande).exists()
        self.assertTrue(commande_exists)

        # Suppression de la commande
        commande.delete()

        # Vérification que la commande n'existe plus
        commande_exists_after_deletion = Commande.objects.filter(pk_Commande=commande.pk_Commande).exists()
        self.assertFalse(commande_exists_after_deletion)