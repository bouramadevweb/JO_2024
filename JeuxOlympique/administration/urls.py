from django.urls import path

from administration import views

urlpatterns = [
    path('list_competition/', views.list_competition, name='list_competition'),
    path('lieu_competition/', views.lieu_competition, name='lieu_competition'),
    path('dates_competitions/',views.dates_competitions, name='dates_competitions'),
    path('competitions/', views.competitions, name='competitions'),
    path('types/', views.types, name='types'),
    path('offres/',views.offres,name='offres'),
    path('commandes/',views.commandes,name='commandes'),
    path('ventes_par_offre',views.ventes_par_offre,name='ventes_par_offre'),
    path('administration/', views.administration, name='administration'),
    path('add_competition/', views.list_competition, name='add_competition'),
    path('update_competition/', views.list_competition, name='update_competition'),
    path('delete_competition/', views.list_competition, name='delete_competition'),
]