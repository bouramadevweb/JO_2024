import pandas as pd
# from JeuxOlympique.settings import DATA_DIR
# from my_app_jo.models import Dates_Competions, List_competition, Lieu_des_competions, ODS
# import os

# def run():
#     file = os.path.join(DATA_DIR, 'data.csv')
#     df = pd.read_csv(file)

#     # Itération sur chaque ligne du DataFrame
#     for index, row in df.iterrows():
#         # Récupération des données de la ligne
#         discipline = row['Discipline']
#         date_debut = row['date_debut']
#         date_fin = row['date_fin']
#         lieu = row['Lieu']
#         capacite = str(row['Capacite'])  # Convertir en chaîne de caractères
#         remises_de_medailles = str(row['Remises_de_médailles'])  # Convertir en chaîne de caractères

#         # Création et sauvegarde de l'instance ODS
#         ods_instance = ODS.objects.create(
#             discipline=discipline,
#             date_debut=date_debut,
#             date_fin=date_fin,
#             lieu=lieu,
#             capacite=capacite,  # Ne convertissez pas la capacité en entier
#             remises_de_medailles=remises_de_medailles
#         )
#         ods_instance.save()

#     print("Données insérées avec succès dans la table ODS.")

# # Appeler la fonction pour insérer les données du CSV dans la table ODS
# if __name__ == "__main__":
#     run()

import pandas as pd
from JeuxOlympique.settings import DATA_DIR
from my_app_jo.models import ODS
import json
import os

def run():
    # Chemin vers le fichier JSON contenant les données
    file_path = os.path.join(DATA_DIR, 'data_2.json')

    # Charger les données JSON dans une liste de dictionnaires
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Itération sur chaque élément de la liste de dictionnaires
    for entry in data:
        # Récupération des données de l'entrée
        discipline = entry['Discipline']
        date_debut = entry['date_debut']
        date_fin = entry['date_fin']
        lieu = entry['Lieu']
        capacite = entry['Capacite']
        
        # Gestion de la clé 'Remises_de_médailles'
        remises_de_medailles = entry.get('Remises_de_médailles', '')

        if isinstance(remises_de_medailles, list):
            remises_de_medailles = ", ".join(remises_de_medailles)

        # Création et sauvegarde de l'instance ODS
        ods_instance = ODS.objects.create(
            discipline=discipline,
            date_debut=date_debut,
            date_fin=date_fin,
            lieu=lieu,
            capacite=capacite,
            remises_de_medailles=remises_de_medailles
        )
        ods_instance.save()

    print("Données insérées avec succès dans la table ODS.")

# Appeler la fonction pour insérer les données JSON dans la table ODS
if __name__ == "__main__":
    run()
