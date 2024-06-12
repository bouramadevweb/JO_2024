from re import template
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls import static
from . import views
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView
from my_app_jo.views import home
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views


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
    path('verificode',views.verificode,name='verificode'),
    path('profile/', views.profile, name='profile'),
    path('modifier_profile',views.modifier_profile,name='modifier_profile' ),
    path('inscription/', views.inscription, name='inscription'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('offresuser/',views.offresuser,name='offresuser'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name ='password_reset_complete.html'), name='password_reset_complete'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()


# handler404 = 'my_app_jo.views.handler404'
