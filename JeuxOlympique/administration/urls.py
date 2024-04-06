from django.urls import path

from administration import views

urlpatterns = [
    path('list_competition/', views.list_competition, name='list_competition'),
    path('lieu_competition/', views.lieu_competition, name='lieu_competition'),
    path('dates_competitions/',views.dates_competitions, name='dates_competitions'),
    path('competitions/', views.competitions, name='competitions'),  # URL pour la vue competitions
    path('add_competition/', views.list_competition, name='add_competition'),
    path('update_competition/', views.list_competition, name='update_competition'),
    path('delete_competition/', views.list_competition, name='delete_competition'),
]