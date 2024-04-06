from my_app_jo.models import Dates_Competions, List_competition, ODS, Lieu_des_competions, Competitions

# Itérer sur chaque enregistrement ODS
for ods_entry in ODS.objects.all():
    # Récupérer l'instance de List_competition associée à cet enregistrement ODS
    try:
        list_competition_instance = List_competition.objects.get(pk_list_competition=ods_entry.discipline.strip())
    except List_competition.DoesNotExist:
        print(f"La discipline '{ods_entry.discipline}' de l'ODS n'existe pas dans la table List_competition.")
        continue

    # Récupérer les instances de Lieu_des_competions associées à cet enregistrement ODS
    lieu_competition_instances = Lieu_des_competions.objects.filter(Nom=ods_entry.lieu)

    # Vérifier s'il y a des instances multiples
    if lieu_competition_instances.count() > 1:
        print(f"Attention : Plusieurs lieux portent le nom '{ods_entry.lieu}' dans la table Lieu_des_competions.")

    # Parcourir toutes les instances de Lieu_des_competions
    for lieu_competition_instance in lieu_competition_instances:
        try:
            # Vérifier si une instance de Dates_Competions avec les mêmes valeurs existe déjà
            dates_competition = Dates_Competions.objects.get(
                pk_list_competition=list_competition_instance,
                pk_lieu=lieu_competition_instance,
                date_debut=ods_entry.date_debut,
                date_fin=ods_entry.date_fin
            )

            # Supprimer les espaces de la clé primaire pour pk_typ_competition
            pk_typ_competition = "_".join([str(lieu_competition_instance.pk_lieu), str(list_competition_instance.pk_list_competition), str(dates_competition.pk_date_competition)])

            # Créer une instance de Competitions avec les valeurs appropriées
            competition, created = Competitions.objects.get_or_create(
                Nom=ods_entry.discipline,
                pk_list_competition=list_competition_instance,
                pk_date_competition=dates_competition,
                pk_lieu=lieu_competition_instance,
                pk_typ_competition=pk_typ_competition.replace(" ", "")
            )

            # Afficher un message pour confirmer l'insertion
            if created:
                print(f"Données insérées pour la compétition : {competition}")

        except Dates_Competions.DoesNotExist:
            print("L'instance de Dates_Competions correspondante n'existe pas.")

print("Toutes les données ont été insérées avec succès.")
