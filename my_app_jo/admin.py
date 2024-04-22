# Dans admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Offre,Types, List_competition, Lieu_des_competions, Dates_Competions, Competitions, Billet, Commande, ODS, Code
from .forms import CustomUserCreationForm

# Enregistrement des modèles dans l'interface d'administration
admin.site.register(Code)
admin.site.register(Types)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = User
    list_display = ['username', 'email','phone_number']
@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('pk_Commande', 'quantite', 'MontantTotal', 'pk_date', 'pk_Offre', 'pk_Utilisateur', 'pk_Billet', 'est_validee')    
@admin.register(Billet)
class BilletAdmin(admin.ModelAdmin):
    list_display = ('pk_Billet', 'Cledebilletelectroniquesecurisee', 'ClefUtilisateur', 'pk_typ_competition', 'est_validee')
@admin.register(Competitions)
class CompetitionsAdmin(admin.ModelAdmin):
    list_display = ('pk_typ_competition', 'Nom', 'pk_list_competition', 'pk_date_competition', 'pk_lieu')

@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('pk_Offre', 'type', 'nombre_personnes', 'prix', 'competition')  
@admin.register(Lieu_des_competions)
class Lieu_des_competionsAdmin(admin.ModelAdmin):
    list_display = ('pk_lieu', 'Nom', 'Ville', 'Capacite', 'Discipline')

@admin.register(Dates_Competions)
class Dates_CompetionsAdmin(admin.ModelAdmin):
    list_display = ('pk_date_competition', 'date_debut', 'date_fin', 'pk_list_competition', 'pk_lieu', 'Remises_de_medailles') 
@admin.register(List_competition)
class List_competitionAdmin(admin.ModelAdmin):
    list_display = ('pk_list_competition', 'nom') 
@admin.register(ODS)
class ODSAdmin(admin.ModelAdmin):
    list_display = ('discipline', 'date_debut', 'date_fin', 'lieu', 'ville', 'capacite', 'remises_de_medailles')
    search_fields = ('discipline', 'lieu', 'ville')
    readonly_fields = ('discipline', 'date_debut', 'date_fin', 'lieu', 'ville', 'capacite', 'remises_de_medailles')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False            
admin.site.register(User, CustomUserAdmin)
