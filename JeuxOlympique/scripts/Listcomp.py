from my_app_jo.models import ODS, List_competition
from django.db import IntegrityError

try:
    for competition_entry in ODS.objects.all():
        print(f"Insertion des données pour {competition_entry.discipline}")
       
        # Création d'une instance de List_competition avec la discipline de ODS
        pk_list_competition = competition_entry.discipline.replace(" ", "_")  # Supprimer tous les espaces

        list_competition_entry = List_competition(
            pk_list_competition=pk_list_competition,
            nom=competition_entry.discipline
        )

        # Enregistrement dans la base de données
        list_competition_entry.save()

    print('Fin d\'insertion des données de la table List_competitions')
except IntegrityError as e:
    print(f"IntegrityError: {e}")
else:
    print('Insertion des données de la table List_competitions terminée avec succès.')
