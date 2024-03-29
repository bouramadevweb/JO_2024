from my_app_jo.models import ODS, Lieu_des_competions, List_competition
from django.db import IntegrityError

try:
    for competition_entry in ODS.objects.all():
        print(f"Insertion des données pour {competition_entry.discipline}")

        # Assurez-vous que la discipline existe
        if competition_entry.discipline:
            # Récupérer l'instance de List_competition associée à la discipline
            discipline_instance, created = List_competition.objects.get_or_create(
                pk_list_competition=competition_entry.discipline,
                defaults={'nom': competition_entry.discipline}
            )

            # Supprimer les espaces dans le nom du lieu pour créer pk_lieu
            pk_lieu = competition_entry.lieu.replace(' ', '')

            # Créer un lieu de compétition en associant la discipline
            lieu_competition = Lieu_des_competions(
                pk_lieu=pk_lieu,
                Nom=competition_entry.lieu,
                Discipline=discipline_instance,
                Capacite=competition_entry.capacite,
                Ville=competition_entry.ville
            )
            lieu_competition.save()

            if created:
                print(f"Données insérées pour {lieu_competition.Nom} avec une nouvelle discipline associée.")
            else:
                print(f"Données insérées pour {lieu_competition.Nom}")
        else:
            print("Aucune discipline n'a été trouvée pour ce lieu de compétition.")

    print("Fin d'insertion des données pour les lieux de compétitions")
except IntegrityError as e:
    print(f"IntegrityError: {e}")
else:
    print("Insertion des données pour les lieux de compétitions terminée avec succès.")
