# Dans admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Offre, Dates_commandes, List_competition, Lieu_des_competions, Dates_Competions, Competitions, Billet, Commande, ODS
from .forms import CustomUserCreationForm

# Enregistrement des modèles dans l'interface d'administration
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = User
    list_display = ['username', 'email']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Offre)
admin.site.register(Dates_commandes)
admin.site.register(List_competition)
admin.site.register(Lieu_des_competions)
admin.site.register(Dates_Competions)
admin.site.register(Competitions)
admin.site.register(Billet)
admin.site.register(Commande)
admin.site.register(ODS)
