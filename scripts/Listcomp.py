from my_app_jo.models import ODS, Lieu_des_competions, List_competition
from django.db import IntegrityError, connection

for competition_entry in ODS.objects.all():
    print(f"Insertion des données pour {competition_entry.discipline}")

        # Assurez-vous que la discipline existe
    if competition_entry.discipline:
            # Récupérer l'instance de List_competition associée à la discipline s'il existe
        discipline_instance, created = List_competition.objects.get_or_create(
        pk_list_competition=competition_entry.discipline.strip().replace(',', '').replace(';', '').replace(' ', ''),
        defaults={'nom': competition_entry.discipline} 
        )
        

    print("Fin d'insertion des données pour les lieux de compétitions")

    