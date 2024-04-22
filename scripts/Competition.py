from my_app_jo.models import List_competition, ODS, Lieu_des_competions, Dates_Competions, Competitions

# Parcourir toutes les entrées ODS
for ods_entry in ODS.objects.all():
    # Rechercher la compétition correspondante dans List_competition
    try:
        list_competition_instance = List_competition.objects.get(nom=ods_entry.discipline.strip())
    except List_competition.DoesNotExist:
        print(f"La compétition avec le nom '{ods_entry.discipline}' de l'ODS n'existe pas dans la table List_competition.")
        continue

    # Rechercher le lieu de compétition correspondant dans Lieu_des_competions
    try:
        lieu_competition_instance = Lieu_des_competions.objects.get(Nom=ods_entry.lieu.strip(), Ville=ods_entry.ville.strip(), Discipline=list_competition_instance)
    except Lieu_des_competions.DoesNotExist:
        print(f"Le lieu de compétition '{ods_entry.lieu}' à '{ods_entry.ville}' pour la compétition '{ods_entry.discipline}' n'existe pas dans la table Lieu_des_competions.")
        continue

    # Rechercher l'instance de Dates_Competions correspondante
    try:
        date_competition_instance = Dates_Competions.objects.get(date_debut=ods_entry.date_debut, date_fin=ods_entry.date_fin, pk_list_competition=list_competition_instance,pk_lieu=lieu_competition_instance)
    except Dates_Competions.DoesNotExist:
        print(f"Les dates de compétition du {ods_entry.date_debut} au {ods_entry.date_fin} pour la compétition '{ods_entry.discipline}' n'existent pas dans la table Dates_Competions.")
        continue
    except Dates_Competions.MultipleObjectsReturned:
        print(f"Plusieurs enregistrements de Dates_Competions correspondent aux mêmes dates de compétition.")
        continue

    # Créer une instance de Competitions avec les valeurs appropriées
    competition = Competitions(
        Nom=list_competition_instance.nom,
        pk_list_competition=list_competition_instance,
        pk_date_competition=date_competition_instance,
        pk_lieu=lieu_competition_instance
    )

    # Sauvegarder l'objet Competitions
    competition.save()

    print(f"Données insérées pour la compétition '{list_competition_instance.nom}' du {ods_entry.date_debut} au {ods_entry.date_fin} à '{ods_entry.lieu}' à '{ods_entry.ville}'")

print("Toutes les données ont été insérées avec succès.")
