from my_app_jo.models import List_competition, ODS, Lieu_des_competions, Dates_Competions

# Parcourir toutes les entrées ODS
for ods_entry in ODS.objects.all():
    # Rechercher la compétition correspondante dans List_competition
    try:
        list_competition_instance = List_competition.objects.get(nom=ods_entry.discipline)
    except List_competition.DoesNotExist:
        print(f"La compétition avec le nom '{ods_entry.discipline}' de l'ODS n'existe pas dans la table List_competition.")
        continue

    # Rechercher le lieu de compétition correspondant dans Lieu_des_competions
    try:
        lieu_competition_instance = Lieu_des_competions.objects.get(Nom=ods_entry.lieu, Ville=ods_entry.ville, Discipline=list_competition_instance)
    except Lieu_des_competions.DoesNotExist:
        print(f"Le lieu de compétition '{ods_entry.lieu}' à '{ods_entry.ville}' pour la compétition '{ods_entry.discipline}' n'existe pas dans la table Lieu_des_competions.")
        continue

    # Créer la clé primaire pour Dates_Competions
    pk_date_competition = f"{ods_entry.date_debut}_{ods_entry.date_fin}_{ods_entry.remises_de_medailles}"

    # Vérifier si l'objet Dates_Competions existe déjà
    if Dates_Competions.objects.filter(pk_date_competition=pk_date_competition).exists():
        print(f"L'objet Dates_Competions pour '{pk_date_competition}' existe déjà.")
        continue

    # Créer l'objet Dates_Competions
    date_competition = Dates_Competions(
        pk_date_competition=pk_date_competition,
        date_debut=ods_entry.date_debut,
        date_fin=ods_entry.date_fin,
        Remises_de_medailles=ods_entry.remises_de_medailles,
        pk_list_competition=list_competition_instance,
        pk_lieu=lieu_competition_instance
    )

    # Sauvegarder l'objet Dates_Competions
    date_competition.save()

    print(f"Données insérées pour la compétition '{ods_entry.discipline}' du {ods_entry.date_debut} au {ods_entry.date_fin} à '{ods_entry.lieu}' à '{ods_entry.ville}'")

print("Toutes les données ont été insérées avec succès.")
