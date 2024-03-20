from my_app_jo.models import Dates_Competions, List_competition, ODS

# Itérer sur chaque enregistrement ODS
for ods_entry in ODS.objects.all():
    # Récupérer l'instance de List_competition associée à cet enregistrement ODS
    try:
        list_competition_instance = List_competition.objects.get(pk_list_competition=ods_entry.discipline)
    except List_competition.DoesNotExist:
        print(f"La discipline '{ods_entry.discipline}' de l'ODS n'existe pas dans la table List_competition.")
        continue

    # Créer une instance de Dates_Competions avec les valeurs appropriées
    date_competition = Dates_Competions(
        date_debut=ods_entry.date_debut,
        date_fin=ods_entry.date_fin,
        pk_list_competition=list_competition_instance,
        Remises_de_medailles=ods_entry.remises_de_medailles
    )

    # Enregistrer l'instance dans la base de données
    date_competition.save()

    # Afficher un message pour confirmer l'insertion
    print(f"Données insérées pour la compétition {list_competition_instance} du {ods_entry.date_debut} au {ods_entry.date_fin}")

print("Toutes les données ont été insérées avec succès.")
