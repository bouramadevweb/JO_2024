from my_app_jo.models import Dates_Competions, List_competition, ODS, Lieu_des_competions
import re

# Fonction pour supprimer tous les espaces d'une chaîne de caractères
def remove_spaces(text):
    return re.sub(r'\s+','_', text)

for ods_entry in ODS.objects.all():
    # Récupérer l'instance de List_competition associée à cet enregistrement ODS
    try:
        list_competition_instance = List_competition.objects.get(pk_list_competition=ods_entry.discipline)
    except List_competition.DoesNotExist:
        print(f"La discipline '{ods_entry.discipline}' de l'ODS n'existe pas dans la table List_competition.")
        continue

    # Supprimer les espaces dans la valeur de pk_list_competition
    # pk_list_competition = remove_spaces(list_competition_instance.pk_list_competition)

    # Récupérer les instances de Lieu_des_competions associées à cet enregistrement ODS
    lieu_competition_instances = Lieu_des_competions.objects.filter(Nom=ods_entry.lieu)

    # Vérifier s'il y a des instances multiples
    if lieu_competition_instances.exists():
        print(f"Attention : Plusieurs lieux portent le nom '{ods_entry.lieu}' dans la table Lieu_des_competions.")

    # Parcourir toutes les instances de Lieu_des_competions
    for lieu_competition_instance in lieu_competition_instances:
        # Créer une instance de Dates_Competions avec les valeurs appropriées
        pk_date_competition = f"{remove_spaces(lieu_competition_instance.Nom)}_{ods_entry.date_debut}_{ods_entry.date_fin}"
        date_competition = Dates_Competions(
            pk_date_competition=remove_spaces(pk_date_competition),
            date_debut=ods_entry.date_debut,
            date_fin=ods_entry.date_fin,
            pk_list_competition=list_competition_instance,
            Remises_de_medailles=ods_entry.remises_de_medailles,
            pk_lieu=lieu_competition_instance
        )

        # Enregistrer l'instance dans la base de données
        date_competition.save()

        # Afficher un message pour confirmer l'insertion
        print(f"Données insérées pour la compétition {list_competition_instance} du {ods_entry.date_debut} au {ods_entry.date_fin} à {lieu_competition_instance.Nom}")

print("Toutes les données ont été insérées avec succès.")
