from my_app_jo.models import ODS, Lieu_des_competions, List_competition

try:
    for competition_entry in ODS.objects.all():
        print(f"Insertion des données pour {competition_entry.discipline}")

        # Assurez-vous que la discipline existe
        if competition_entry.discipline:
            # Récupérer l'instance de List_competition associée à la discipline
            discipline_instance = List_competition.objects.get(pk_list_competition=competition_entry.discipline)
            
            # Créer un lieu de compétition en associant la discipline
            lieu_competition = Lieu_des_competions(
                Nom=competition_entry.lieu,
                Discipline=discipline_instance,
                Capacite=competition_entry.capacite
            )
            lieu_competition.save()
            print(f"Données insérées pour {lieu_competition.Nom}")
        else:
            print("Aucune discipline n'a été trouvée pour ce lieu de compétition.")

    print('Fin d\'insertion des données pour les lieux de compétitions')
except IntegrityError as e:
    print(f"IntegrityError: {e}")
else:
    print('Insertion des données pour les lieux de compétitions terminée avec succès.')
