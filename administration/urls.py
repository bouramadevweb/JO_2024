from django.urls import path
from administration import views
from .views import AdminCreateView,login
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/create/', AdminCreateView.as_view(), name='admin_create'),
    path('login/', login , name='login'),
    path('admindeconnexion/',views.admindeconnexion, name='admindeconnexion'),
    path('users/', views.users, name='users'),
    path('administration/', views.administration, name='administration'),
    
    path('list_competition/', views.list_competition, name='list_competition'),
    path('lieu_competition/', views.lieu_competition, name='lieu_competition'),
    path('dates_competitions/',views.dates_competitions, name='dates_competitions'),
    path('competitions/', views.competitions, name='competitions'),
    path('types/', views.types, name='types'),
    path('offres/',views.offres,name='offres'),
    path('commandes/',views.commandes,name='commandes'),
    path('ventes_par_offre',views.ventes_par_offre,name='ventes_par_offre'),
    path('add_competition/', views.list_competition, name='add_competition'),
    path('update_competition/', views.list_competition, name='update_competition'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('delete_competition/', views.list_competition, name='delete_competition'),
    path('admin_profile/', views.admin_profile, name ='admin_profile'),
    path('admin_modifier_profile',views.admin_modifier_profile, name = 'admin_modifier_profile'),

    # path('admin/password_reset/', auth_views.PasswordResetView.as_view(template_name='admin/password_reset_form.html'), name='password_reset'),

    # path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='admin/password_reset_done.html'), name='password_reset_done'),
    # path('admin/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('admin/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
