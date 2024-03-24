from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls import static

urlpatterns = [
    path('', views.home, name='home'),
    path('choisir_ticket/', views.choisir_ticket, name='choisir_ticket'),
    path('voir_panier/', views.voir_panier, name='voir_panier'),
    path('get_offres/', views.get_offres, name='get_offres'),
    path('connexion/', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('passer_commande/<str:offre_id>/', views.passer_commande, name='passer_commande'),
     path('deconnexion/', views.deconnexion, name='deconnexion'),
]
