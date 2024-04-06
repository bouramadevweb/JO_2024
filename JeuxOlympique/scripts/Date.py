from my_app_jo.models import Dates_Competions, List_competition, ODS, Lieu_des_competions

def remove_spaces(text):
    return text.replace(' ', '')

def remove_punctuation(text):
    return text.replace(',', '').replace(';', '')

for ods_entry in ODS.objects.all():
    try:
        list_competition_instance = List_competition.objects.get(pk_list_competition=ods_entry.discipline)
    except List_competition.DoesNotExist:
        print(f"La discipline '{ods_entry.discipline}' de l'ODS n'existe pas dans la table List_competition.")
        continue

    pk_list_competition = remove_spaces(list_competition_instance.pk_list_competition)

    lieu_competition_instances = Lieu_des_competions.objects.filter(Nom=ods_entry.lieu)

    if lieu_competition_instances.exists():
        print(f"Attention : Plusieurs lieux portent le nom '{ods_entry.lieu}' dans la table Lieu_des_competions.")

    for lieu_competition_instance in lieu_competition_instances:
        pk_date_competition = f"{remove_punctuation(remove_spaces(lieu_competition_instance.Nom))}{ods_entry.date_debut}{ods_entry.date_fin}"
        pk_date_competition = remove_spaces(pk_date_competition.strip())  # Supprimer les espaces et appels à strip()
        date_competition = Dates_Competions(
            pk_date_competition=remove_punctuation(pk_date_competition),
            date_debut=ods_entry.date_debut,
            date_fin=ods_entry.date_fin,
            pk_list_competition=list_competition_instance,
            Remises_de_medailles=ods_entry.remises_de_medailles,
            pk_lieu=lieu_competition_instance
        )

        date_competition.save()

        print(f"Données insérées pour la compétition {list_competition_instance} du {ods_entry.date_debut} au {ods_entry.date_fin} à {lieu_competition_instance.Nom.strip()}")

print("Toutes les données ont été insérées avec succès.")
