from my_app_jo.models import ODS, Lieu_des_competions, List_competition
from django.db import IntegrityError

try:
    # Insertion des données pour les lieux de compétitions
    for ods_instance in ODS.objects.all():
        print(f"Insertion des données pour {ods_instance.discipline}")
        discipline_instance = List_competition.objects.get(nom=ods_instance.discipline)
        pk_lieus = f"{ods_instance.ville},{ods_instance.lieu},{ods_instance.capacite},{discipline_instance.nom}"
        pk_lieus = pk_lieus.replace(',', '').replace(';', '').replace(' ', '').replace('-', '')
        # Assurez-vous que la discipline existe
        
        # Créer un lieu de compétition en associant la discipline
        lieu_competition = Lieu_des_competions(
            pk_lieu=pk_lieus,  # Supprimer les espaces
            Nom=ods_instance.lieu.strip(),  # Supprimer les espaces
            Discipline=discipline_instance,
            Capacite=ods_instance.capacite,
            Ville=ods_instance.ville
        )

        lieu_competition.save()

    print("Fin d'insertion des données pour les lieux de compétitions")

except IntegrityError as e:
    print(f"IntegrityError: {e}")

except Exception as e:
    print(f"Une erreur s'est produite : {e}")
