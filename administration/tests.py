from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()  # Utilisez le modèle d'utilisateur personnalisé

class LoginViewTestCase(TestCase):
    """Test pour la vue de connexion"""

    def setUp(self):
        self.client = Client()
        # Créer un utilisateur pour les tests

    def test_login_with_valid_credentials(self):
        # Simule une requête POST avec des identifiants valides
        response = self.client.post(reverse('login'), {
            'username': 'admin',
            'password': 'adminpassword'
        }, follow=True)  # Suivre la redirection

        # Vérifie que la réponse est une redirection vers 'administration'
        self.assertRedirects(response, reverse('administration'))

    def test_login_with_invalid_credentials(self):
        # Simule une requête POST avec des identifiants invalides
        response = self.client.post(reverse('login'), {
            'username': 'admin',
            'password': 'wrongpassword'
        })

        # Vérifie que le statut de la réponse est 200 (la page de connexion est rechargée)
        self.assertEqual(response.status_code, 200)
        # Vérifie que le template utilisé est bien 'admin/login.html'
        self.assertTemplateUsed(response, 'admin/login.html')
        # Vérifie que le formulaire contient un message d'erreur
        self.assertContains(response, "Veuillez entrer un nom d'utilisateur et un mot de passe valides.")
