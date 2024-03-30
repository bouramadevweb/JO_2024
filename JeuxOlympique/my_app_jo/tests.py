from django.test import TestCase,Client
from .models import Competitions ,Lieu_des_competions,List_competition,Dates_Competions,Offre
from datetime import datetime
from django.utils import timezone

from django.urls import reverse

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
