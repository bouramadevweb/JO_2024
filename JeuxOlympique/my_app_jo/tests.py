from django.test import TestCase,Client
from django.test import TestCase, RequestFactory
from .models import Competitions ,Lieu_des_competions,List_competition,Dates_Competions,Offre,Commande,User,Billet
from datetime import datetime
from django.utils import timezone
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import User
import qrcode, base64
from io import BytesIO
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Offre, Commande, Billet, Competitions


class ListCompetitionCRUDTestCase(TestCase):
    """_summary_

    Args:
        TestCase (_type_): test CRUD list de competition
    """
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
    """_summary_

    Args:
        TestCase (_type_): Test CRUD lieux de competition
    """
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
    """_summary_

    Args:
        TestCase (_type_): Test CRUD Dates de Compétition
    """
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

        # Comparer la clé primaire de l'instance nouvellement crée avec la valeur attendue
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
    """_summary_

    Args:
        TestCase (_type_): test CRUD competition
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

class OffreCRUDTestCase(TestCase):
    """_summary_

    Args:
        TestCase (_type_): Test Crud Offre
    """
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
    """_summary_

    Args:
        TestCase (_type_): test CRUD Billet
    """

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
    """_summary_

    Args:
        TestCase (_type_): test CRUD Commande
    """
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

class AjouterAuPanierTestCase(TestCase):
    """_summary_

    Args:
        TestCase (_type_):test views modifier commande
    """
    def setUp(self):
        # Créer un utilisateur
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Créer quelques instances de compétition et d'offre
        list_competition = List_competition.objects.create(pk_list_competition='comp_1', nom='Compétition 1')
        lieu_competition = Lieu_des_competions.objects.create(pk_lieu='lieu_1', Nom='Lieu 1', Ville='Ville 1', Capacite=100, Discipline=list_competition)
        date_competition = Dates_Competions.objects.create(pk_date_competition='date_1', date_debut='2024-08-01', date_fin='2024-08-11', pk_list_competition=list_competition, pk_lieu=lieu_competition)

        self.list_competition = list_competition
        self.lieu_competition = lieu_competition
        self.date_competition = date_competition

        self.competition = Competitions.objects.create(Nom='Compétition de test', pk_list_competition=self.list_competition, pk_date_competition=self.date_competition, pk_lieu=self.lieu_competition)

        self.offre = Offre.objects.create(type='Une', nombre_personnes=1, prix=10.0, competition=self.competition)

    def test_ajouter_au_panier(self):
        # Connecter l'utilisateur
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        # Envoyer une requête POST à la vue ajouter_au_panier
        response = self.client.post(reverse('ajouter_au_panier'), {'offre_id': [self.offre.pk_Offre], 'quantite_{}'.format(self.offre.pk_Offre): 2})

        # Vérifier si la réponse est une redirection vers 'voir_panier'
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('voir_panier'))

        # Vérifier si une instance de Commande et de Billet a été créée
        self.assertEqual(Commande.objects.count(), 1)
        commandes = Commande.objects.all()
        self.assertEqual(Billet.objects.count(), 2)  # Supposant que deux instances de Billet sont créées

        # Vérifier si la Commande créée est associée à l'utilisateur connecté
        commande = commandes.first()
        self.assertEqual(commande.pk_Utilisateur, self.user)

        # Vérifier si les Billets créés sont associés à la bonne compétition
        for billet in Billet.objects.all():
            self.assertEqual(billet.pk_typ_competition, self.competition)

class VoirPanierTestCase(TestCase):
    """_summary_

    Args:
        TestCase (_type_): test views pour voir le panier
    """
    def setUp(self):
        # Créer un utilisateur
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Connecter l'utilisateur
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        # Créer quelques instances de compétition et d'offre
        self.list_competition = List_competition.objects.create(pk_list_competition='comp_1', nom='Compétition 1')
        self.lieu_competition = Lieu_des_competions.objects.create(pk_lieu='lieu_1', Nom='Lieu 1', Ville='Ville 1', Capacite=100, Discipline=self.list_competition)
        self.date_competition = Dates_Competions.objects.create(pk_date_competition='date_1', date_debut='2024-08-01', date_fin='2024-08-11', pk_list_competition=self.list_competition, pk_lieu=self.lieu_competition)

        self.competition = Competitions.objects.create(Nom='Test Competition', pk_list_competition=self.list_competition, pk_date_competition=self.date_competition, pk_lieu=self.lieu_competition)

        self.offre = Offre.objects.create(type='Une', nombre_personnes=1, prix=10.0, competition=self.competition)

        # Créer une commande pour l'utilisateur
        self.commande = Commande.objects.create(quantite=1, MontantTotal=10.0, pk_Offre=self.offre, pk_Utilisateur=self.user)

    def test_voir_panier(self):
        # Envoyer une requête GET à la vue voir_panier
        response = self.client.get(reverse('voir_panier'))

        # Vérifier que la réponse est réussie (code 200)
        self.assertEqual(response.status_code, 200)

        # Vérifier que la commande de l'utilisateur est présente dans le contexte de la réponse
        self.assertIn(self.commande, response.context['commandes'])

        # Vérifier que les informations de la commande sont affichées correctement dans le template
        self.assertContains(response, str(self.commande.quantite))
        self.assertContains(response, str(self.commande.MontantTotal))


class modifierCommandeTestCase(TestCase):
    """_summary_

    Args:
        TestCase (_type_): test views modifier Commande
    """
    def setUp(self):
        # Créer une commande et une offre pour le test
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.list_competition = List_competition.objects.create(pk_list_competition='comp_1', nom='Compétition 1')
        self.lieu_competition = Lieu_des_competions.objects.create(pk_lieu='lieu_1', Nom='Lieu 1', Ville='Ville 1', Capacite=100, Discipline=self.list_competition)
        self.date_competition = Dates_Competions.objects.create(pk_date_competition='date_1', date_debut='2024-08-01', date_fin='2024-08-11', pk_list_competition=self.list_competition, pk_lieu=self.lieu_competition)

        self.competition = Competitions.objects.create(Nom='Test Competition', pk_list_competition=self.list_competition, pk_date_competition=self.date_competition, pk_lieu=self.lieu_competition)

        self.offre = Offre.objects.create(type='Une', nombre_personnes=1, prix=10.0, competition=self.competition)

        # Créer une commande pour l'utilisateur
        self.commande = Commande.objects.create(quantite=1, MontantTotal=10.0, pk_Offre=self.offre, pk_Utilisateur=self.user)

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
    """_summary_

    Args:
        TestCase (_type_): Test CRUD supprimer pour commande
    """
    def setUp(self):
        # Créer un utilisateur
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Créer une commande pour l'utilisateur
        self.commande = Commande.objects.create(quantite=1, MontantTotal=10.0, pk_Utilisateur=self.user)
        self.list_competition = List_competition.objects.create(pk_list_competition='comp_1', nom='Compétition 1')
        self.lieu_competition = Lieu_des_competions.objects.create(pk_lieu='lieu_1', Nom='Lieu 1', Ville='Ville 1', Capacite=100, Discipline=self.list_competition)
        self.date_competition = Dates_Competions.objects.create(pk_date_competition='date_1', date_debut='2024-08-01', date_fin='2024-08-11', pk_list_competition=self.list_competition, pk_lieu=self.lieu_competition)

        self.competition = Competitions.objects.create(Nom='Test Competition', pk_list_competition=self.list_competition, pk_date_competition=self.date_competition, pk_lieu=self.lieu_competition)

        self.offre = Offre.objects.create(type='Une', nombre_personnes=1, prix=10.0, competition=self.competition)

        # Créer une commande pour l'utilisateur
        self.commande = Commande.objects.create(quantite=1, MontantTotal=10.0, pk_Offre=self.offre, pk_Utilisateur=self.user)

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
        
        # Vérifier que le message de succès est affiché
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "success")
        self.assertEqual(messages[0].message, "La commande a été supprimée avec succès.")   

class SupprimerCommandeTestCase(TestCase):
    """_summary_

    Args:
        TestCase (_type_): test de views pour supprimmer une commande
    """
    def setUp(self):
        # Créer un utilisateur
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Créer une compétition
        self.list_competition = List_competition.objects.create(pk_list_competition='comp_1', nom='Compétition 1')
        self.lieu_competition = Lieu_des_competions.objects.create(pk_lieu='lieu_1', Nom='Lieu 1', Ville='Ville 1', Capacite=100, Discipline=self.list_competition)
        self.date_competition = Dates_Competions.objects.create(pk_date_competition='date_1', date_debut='2024-08-01', date_fin='2024-08-11', pk_list_competition=self.list_competition, pk_lieu=self.lieu_competition)
        self.competition = Competitions.objects.create(Nom='Test Competition', pk_list_competition=self.list_competition, pk_date_competition=self.date_competition, pk_lieu=self.lieu_competition)

        # Créer une offre pour la compétition
        self.offre = Offre.objects.create(type='Une', nombre_personnes=1, prix=10.0, competition=self.competition)

        # Créer une commande pour l'utilisateur avec l'offre
        self.commande = Commande.objects.create(quantite=1, MontantTotal=10.0, pk_Offre=self.offre, pk_Utilisateur=self.user)

        # Se connecter en tant qu'utilisateur pour simuler une requête
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_supprimer_commande(self):
        # Définir l'URL pour la vue supprimer_commande avec l'ID de commande comme paramètre
        url = reverse('supprimer_commande', kwargs={'commande_id': self.commande.pk})
        
        # Envoyer une requête POST pour supprimer la commande
        response = self.client.post(url)
        print(response)
        # Vérifier que la réponse redirige vers la vue voir_panier
        self.assertRedirects(response, reverse('voir_panier'))
        
        # Vérifier que la commande a été supprimée de la base de données
        self.assertFalse(Commande.objects.filter(pk=self.commande.pk).exists())


class DetailsBilletTestCase(TestCase):
    """_summary_

    Args:
        TestCase (_type_): Test pour billet en details
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='password')
        self.list_competition = List_competition.objects.create(pk_list_competition='Football', nom='Football')
        self.lieu_des_competions = Lieu_des_competions.objects.create(pk_lieu='Paris_Stade_10000_Football', Nom='Stade de Paris', Ville='Paris', Capacite=10000, Discipline=self.list_competition)
        self.dates_competions = Dates_Competions.objects.create(pk_date_competition='Football_Paris_Stade_2024-08-01_2024-08-11', date_debut=timezone.now(), date_fin=timezone.now(), pk_list_competition=self.list_competition, 
                                                                pk_lieu=self.lieu_des_competions, 
                                                                Remises_de_medailles='Some medals')
        self.competition = Competitions.objects.create(Nom='Test Competition', pk_list_competition=self.list_competition,
                                                        pk_date_competition=self.dates_competions,
                                                          pk_lieu=self.lieu_des_competions)
        self.offre = Offre.objects.create(type='One', nombre_personnes=1, prix=10.0, competition=self.competition)
        self.billet = Billet.objects.create(pk_typ_competition=self.competition, ClefUtilisateur=123, Cledebilletelectroniquesecurisee=456)
        self.commande = Commande.objects.create(quantite=2, MontantTotal=50.0, pk_Offre=self.offre, pk_Utilisateur=self.user)
        self.billet.commande_set.add(self.commande)
    
    def test_details_billet(self):
        # Définir l'URL pour la vue details_billet avec l'ID de billet comme paramètre
        url = reverse('details_billet', kwargs={'billet_id': self.billet.pk})

        # Envoyer une requête GET pour obtenir les détails du billet
        response = self.client.get(url)

        # Vérifier que la réponse a un statut HTTP 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Vérifier que les détails du billet sont présents dans la réponse
        self.assertContains(response, str(self.billet.ClefUtilisateur))
        self.assertContains(response, str(self.billet.Cledebilletelectroniquesecurisee))

class inscription_connexion_deconnexionTestCase(TestCase):
    def setUp(self):
        # Créer un utilisateur pour les tests
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Créer des offres pour les tests
        
        self.list_competition = List_competition.objects.create(pk_list_competition='comp_1', nom='Compétition 1')
        self.lieu_competition = Lieu_des_competions.objects.create(pk_lieu='lieu_1', Nom='Lieu 1', Ville='Ville 1', Capacite=100, Discipline=self.list_competition)
        self.date_competition = Dates_Competions.objects.create(pk_date_competition='date_1', date_debut='2024-08-01', date_fin='2024-08-11', pk_list_competition=self.list_competition, pk_lieu=self.lieu_competition)
        self.competition = Competitions.objects.create(Nom='Test Competition', pk_list_competition=self.list_competition, pk_date_competition=self.date_competition, pk_lieu=self.lieu_competition)

        # Créer une offre pour la compétition
        self.offre = Offre.objects.create(type='Une', nombre_personnes=1, prix=10.0, competition=self.competition)

        # Créer une commande pour l'utilisateur avec l'offre
        self.commande = Commande.objects.create(quantite=1, MontantTotal=10.0, pk_Offre=self.offre, pk_Utilisateur=self.user)

        # Se connecter en tant qu'utilisateur pour simuler une requête
    def test_inscription_view(self):
        # Tester la vue d'inscription avec une requête POST valide
        response = self.client.post(reverse('inscription'), {'username': 'newuser', 'password1': 'newpassword', 'password2': 'newpassword'})
        self.assertEqual(response.status_code, 200)  # Redirection après une inscription réussie

    def test_connexion_view(self):
        # Tester la vue de connexion avec une requête POST valide
        response = self.client.post(reverse('connexion'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Redirection après une connexion réussie

    def test_deconnexion_view(self):
        # Se connecter d'abord
        self.client.login(username='testuser', password='testpassword')

        # Tester la vue de déconnexion
        response = self.client.get(reverse('deconnexion'))
        self.assertEqual(response.status_code, 302)  # Redirection après une déconnexion réussie

    def test_ventes_par_offre_view(self):
        # Créer un utilisateur administrateur pour accéder à la vue admin
        admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword')
        self.client.login(username='admin', password='adminpassword')

        # Tester la vue ventes_par_offre
        response = self.client.get(reverse('ventes_par_offre'))
        self.assertEqual(response.status_code, 200)