from django.urls import path

from administration import views

urlpatterns = [
    path('list_competition/', views.list_competition, name='list_competition'),
    path('add_competition/', views.list_competition, name='add_competition'),
    path('update_competition/', views.list_competition, name='update_competition'),
    path('delete_competition/', views.list_competition, name='delete_competition'),
]