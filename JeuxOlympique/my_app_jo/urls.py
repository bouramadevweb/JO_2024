from django.urls import path
from . import views
# from .views import deconnexion

urlpatterns = [
    path('', views.home, name='home'),
    path('choisir_ticket/', views.choisir_ticket, name='choisir_ticket'),
    path('connexion/', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('passer_commande/<str:offre_id>/', views.passer_commande, name='passer_commande'),
     path('deconnexion/', views.deconnexion, name='deconnexion'),
]
