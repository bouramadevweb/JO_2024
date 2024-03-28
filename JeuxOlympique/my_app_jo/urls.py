from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls import static

urlpatterns = [
    path('', views.home, name='home'),
    path('choisir_ticket/', views.choisir_ticket, name='choisir_ticket'),
    path('ajouter_au_panier/',views.ajouter_au_panier,name='ajouter_au_panier'),
    path('voir_panier/', views.voir_panier, name='voir_panier'),
    path('modifier_commande/<int:commande_id>/', views.modifier_commande, name='modifier_commande'),
    path('valider_commande/<int:commande_id>/',views.valider_commande,name='valider_commande'),
    path('payer_commande/<int:command_id>/', views.payer_commande, name='payer_commande'),
    path('supprimer_commande/<int:commande_id>/',views.supprimer_commande,name='supprimer_commande'),
    path('connexion/', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
]
