from django.test import TestCase

# Create your tests here.
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.test import TestCase, RequestFactory
from my_app_jo.models import User,Competitions,List_competition,Lieu_des_competions,Types,Offre, Types, Competitions,Dates_Competions
from django.contrib.auth import get_user_model  # Importez get_user_model pour obtenir le modèle utilisateur personnalisé

from django.test import TestCase, RequestFactory
from django.urls import reverse
from .views import offres
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.test import TestCase, Client
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.test import TestCase, Client
from django.urls import reverse
# from .models import List_competition,Lieu_des_competions
from .form import ListCompetitionForm
from django.test import TestCase, RequestFactory
from django.urls import reverse
from my_app_jo.models import List_competition
from .form import ListCompetitionForm
from .views import list_competition,lieu_competition,dates_competitions,competitions
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .form import CompetitionForm, TypesForm

class AdminLoginViewTest(TestCase):
    def setUp(self):
        # Crée un client de test
        self.client = Client()
        # Crée un superutilisateur de test
        User = get_user_model()
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )

    def test_admin_login(self):
        # Crée une requête POST avec les identifiants du superutilisateur
        data = {'username': 'admin', 'password': 'adminpassword'}
        response = self.client.post(reverse('login'), data)  # Utilise le client pour envoyer la requête POST

        # Vérifie que la vue redirige après une authentification réussie
        self.assertEqual(response.status_code, 302)
         # Vérifie que la redirection est correcte
        self.assertRedirects(response, reverse('administration')) 

    def test_admin_login_invalid_password(self):
        # Crée une requête POST avec un mot de passe incorrect
        data = {'username': 'admin', 'password': 'wrongpassword'}
        response = self.client.post(reverse('login'), data)  # Utilise le client pour envoyer la requête POST

        # Vérifie que la vue renvoie un statut 200 et affiche le formulaire avec une erreur
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'admin/login.html')

    def test_admin_logout(self):
        # Appelle la vue de déconnexion
        response = self.client.get(reverse('admindeconnexion'))
        
        # Vérifie que la vue redirige vers la page de connexion
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        # Vérifie que l'utilisateur est déconnecté
        response = self.client.get(reverse('admin:login'))
        self.assertNotIn('_auth_user_id', self.client.session)







class CompetitionListViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.list_competition_url = reverse('list_competition')
        
        # Create a user for simulating authentication
        User = get_user_model()
        self.admin = User.objects.create_superuser(
            username='admins',
            email='admins@example.com',
            password='adminpassword'
        )

    def test_get_request(self):
        request = self.factory.get(self.list_competition_url)
        request.user = self.admin 
        response = list_competition(request)
        self.assertEqual(response.status_code, 200)
    
    def test_post_add_request(self):
        request = self.factory.post(self.list_competition_url, {'add': ''})
        request.user = self.admin  
        response = list_competition(request)
        self.assertEqual(response.status_code, 302)  
    
    def test_post_update_request(self):
        # Create a competition instance for updating
        competition  = List_competition.objects.create(pk_list_competition='escrime',
                                                                nom='escrime')
        request = self.factory.post(self.list_competition_url, {'update': '', 'id': competition.pk_list_competition})
        request.user = self.admin  
        response = list_competition(request)
        # Assuming successful update redirects
        self.assertEqual(response.status_code, 302)  
    
    def test_post_delete_request(self):
        # Create a competition instance for deleting
        competition =  List_competition.objects.create(pk_list_competition='kungfu',
                                                                nom='kungfu')
        request = self.factory.post(self.list_competition_url, {'delete': '', 'id': competition.pk_list_competition})
        request.user = self.admin  
        response = list_competition(request)
        self.assertEqual(response.status_code, 302)

class LieuCompetitionViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.lieu_competition_url = reverse('lieu_competition')
        User = get_user_model()
        self.admin = User.objects.create_superuser(
            username='admins_2',
            email='admins_2@example.com',
            password='adminpassword'
        )
        self.list_competition  = List_competition.objects.create(pk_list_competition='escrime',
                                                                nom='escrime')
        self.lieu_competition = Lieu_des_competions.objects.create(pk_lieu='paris_escrime',
                                                                   Nom='escrime club', 
                                                                   Ville='Paris',
                                                                   Capacite=100,
                                                                   Discipline=self.list_competition)
    def test_get_request(self):
        request = self.factory.get(self.lieu_competition_url)
        request.user = self.admin 
        response = lieu_competition(request)
        self.assertEqual(response.status_code, 200)
    
    def test_post_add_request(self):
        request = self.factory.post(self.lieu_competition_url, {'add': ''})
        request.user = self.admin
        response = lieu_competition(request)
        self.assertEqual(response.status_code, 302)  
    
    def test_post_update_request(self):
        lieu =  Lieu_des_competions.objects.create(pk_lieu='clermont_escrime',
                                                                   Nom='escrime clubs', 
                                                                   Ville='clermont ferrand',
                                                                   Capacite=100,
                                                                   Discipline=self.list_competition)
        request = self.factory.post(self.lieu_competition_url, {'update': '', 'id': lieu.pk_lieu})
        request.user = self.admin
        response = lieu_competition(request)
        self.assertEqual(response.status_code, 302)  
    
    def test_post_delete_request(self):
        lieu  = Lieu_des_competions.objects.create(pk_lieu='limoge',
                                                   Nom='escrime limoge', 
                                                    Ville='limoge',
                                                     Capacite=100,
                                                     Discipline=self.list_competition)
        request = self.factory.post(self.lieu_competition_url, {'delete': '', 'id': lieu.pk_lieu})
        request.user = self.admin
        response = lieu_competition(request)
        self.assertEqual(response.status_code, 302)

class DatesCompetitionsViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.dates_competitions_url = reverse('dates_competitions')  # Assurez-vous que l'URL name est correcte
        User = get_user_model()
        self.admin = User.objects.create_superuser(
            username='admins_3',
            email='admins_3@example.com',
            password='adminpassword'
        )
        self.list_competition  = List_competition.objects.create(pk_list_competition='escrimes',
                                                                nom='escrimes')
        self.lieu_competition = Lieu_des_competions.objects.create(pk_lieu='Lyon_escrimes',
                                                                   Nom='escrime Lyon club', 
                                                                   Ville='lyon',
                                                                   Capacite=200,
                                                                   Discipline=self.list_competition)
        self.date_competition = Dates_Competions.objects.create(pk_date_competition='date_3',
                                                                date_debut='2024-09-02',
                                                                date_fin='2024-09-12',
                                                                pk_list_competition=self.list_competition,
                                                                pk_lieu=self.lieu_competition)
    def test_get_request(self):
        request = self.factory.get(self.dates_competitions_url)
        request.user = self.admin
        response = dates_competitions(request)
        self.assertEqual(response.status_code, 200)
    
    def test_post_add_request(self):
        request = self.factory.post(self.dates_competitions_url, {'add': '', 'date': '2024-05-26', 'name': 'Test Date'})
        request.user = self.admin
        response = dates_competitions(request)
        self.assertEqual(response.status_code, 302)  
    
    def test_post_update_request(self):
        # Créez une instance de date de compétition pour la mise à jour
        date_competition = self.date_competition = Dates_Competions.objects.create(pk_date_competition='date_3',
                                                                date_debut='2024-07-02',
                                                                date_fin='2024-07-12',
                                                                pk_list_competition=self.list_competition,
                                                                pk_lieu=self.lieu_competition)
        request = self.factory.post(self.dates_competitions_url, {'update': '', 'id': date_competition.pk_date_competition, 'date': '2024-05-27', 'name': 'Updated Test Date'})
        request.user = self.admin
        response = dates_competitions(request)
        self.assertEqual(response.status_code, 302)  
    
    def test_post_delete_request(self):
        self.list_competition  = List_competition.objects.create(pk_list_competition='escrimes femme',
                                                                nom='escrimes femme')
        self.lieu_competition = Lieu_des_competions.objects.create(pk_lieu='grenoble_escrimes',
                                                                   Nom='escrime grenoble club', 
                                                                   Ville='grenoble',
                                                                   Capacite=200,
                                                                   Discipline=self.list_competition)
        # Créez une instance de date de compétition pour la suppression
        date_competition = Dates_Competions.objects.create(pk_date_competition='date_4',
                                                                date_debut='2024-01-02',
                                                                date_fin='2024-09-11',
                                                                pk_list_competition=self.list_competition,
                                                                pk_lieu=self.lieu_competition)
        request = self.factory.post(self.dates_competitions_url, {'delete': '', 'id': date_competition.pk_date_competition})
        request.user = self.admin
        response = dates_competitions(request)
        self.assertEqual(response.status_code, 302)


class CompetitionsViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.competitions_url = reverse('competitions')
        
        self.list_competition = List_competition.objects.create(
            pk_list_competition='escrime_hommes',
            nom='Escrime Hommes'
        )
        
        self.lieu_competition = Lieu_des_competions.objects.create(
            pk_lieu='issoir_escrimes',
            Nom='Escrime Club', 
            Ville='Issoir',
            Capacite=100,
            Discipline=self.list_competition
        )
        
        self.date_competition = Dates_Competions.objects.create(
            pk_date_competition='date_12',
            date_debut='2024-09-02',
            date_fin='2024-09-12',
            pk_list_competition=self.list_competition,
            pk_lieu=self.lieu_competition
        )

        self.competition = Competitions.objects.create(
            pk_typ_competition='_issoir_escrimes',
            Nom='Escrime Hommes',
            pk_list_competition=self.list_competition, 
            pk_date_competition=self.date_competition, 
            pk_lieu=self.lieu_competition
        )

        User = get_user_model()
        self.admin = User.objects.create_superuser(
            username='admin_3',
            email='admin_3@example.com',
            password='adminpassword'
        )

    def test_get_request(self):
        request = self.factory.get(self.competitions_url)
        request.user = self.admin
        response = competitions(request)
        self.assertEqual(response.status_code, 200)

   