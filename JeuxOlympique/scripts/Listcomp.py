from my_app_jo.models import ODS, List_competition
from django.db import connection
from django.db import IntegrityError

try:
    # Récupérer toutes les entrées de List_competition
    list_competitions = List_competition.objects.all()

    # Pour chaque instance de List_competition, appliquer la mise à jour
    for competition in list_competitions:
        # Appliquer la mise à jour en utilisant la méthode save() de l'instance
        competition.pk_list_competition = competition.pk_list_competition.replace(' ', '')  # Supprimer les espaces
        competition.save()

    print('Mise à jour des données de la table List_competition terminée avec succès.')
except IntegrityError as e:
    print(f"IntegrityError: {e}")


# try:
#     # Exécution de la requête SQL brute pour mettre à jour les données
#     with connection.cursor() as cursor:
#         cursor.execute("UPDATE my_app_jo_list_competition SET pk_list_competition = REPLACE(pk_list_competition, ' ', '')")

#     print('Mise à jour des données de la table List_competition terminée avec succès.')
# except Exception as e:
#     print(f"Une erreur s'est produite lors de la mise à jour des données : {e}")
