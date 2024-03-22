# Dans admin.py
from django.contrib import admin
from .models import Offre, User, Dates_commandes, List_competition, Lieu_des_competions, Dates_Competions, Competitions, Billet, Commande, ODS

# Enregistrement des modèles dans l'interface d'administration
admin.site.register(Offre)
admin.site.register(User)
admin.site.register(Dates_commandes)
admin.site.register(List_competition)
admin.site.register(Lieu_des_competions)
admin.site.register(Dates_Competions)
admin.site.register(Competitions)
admin.site.register(Billet)
admin.site.register(Commande)
admin.site.register(ODS)
