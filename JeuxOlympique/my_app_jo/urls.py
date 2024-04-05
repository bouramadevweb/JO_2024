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
    path('payer_commande/<int:commande_id>/', views.payer_commande, name='payer_commande'),
    path('supprimer_commande/<int:commande_id>/',views.supprimer_commande,name='supprimer_commande'),
    path('mes_billets/', views.mes_billets, name='mes_billets'),
    path('billet/<int:billet_id>/', views.details_billet, name='details_billet'),
    path('connexion/', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('ventes_par_offre/', views.ventes_par_offre, name='ventes_par_offre'),
    # path('lister_competitions',views.lister_competitions,name="lister_competitions")
]
