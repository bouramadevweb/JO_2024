from django.db import connection

try:
    # Exécution de la requête SQL brute pour mettre à jour les données
    with connection.cursor() as cursor:
        cursor.execute("UPDATE my_app_jo_list_competition SET pk_list_competition = REPLACE(pk_list_competition, \' \', \'\')")

    print('Mise à jour des données de la table List_competition terminée avec succès.')
except Exception as e:
    print(f"Une erreur s'est produite lors de la mise à jour des données : {e}")


try:
    with connection.cursor() as cursor:
        # Mettre à jour pk_lieu en supprimant les espaces
        cursor.execute("UPDATE my_app_jo_lieu_des_competions SET pk_lieu = REPLACE(pk_lieu, ' ', '')")

        # Mettre à jour la clé étrangère Discipline en supprimant les espaces

    print('Mise à jour des données de la table Lieu_des_competions terminée avec succès.')
except Exception as e:
    print(f"Une erreur s'est produite lors de la mise à jour des données : {e}")





try:
    with connection.cursor() as cursor:
        # Mettre à jour pk_date_competition en supprimant les espaces
        cursor.execute("UPDATE my_app_jo_dates_competions SET pk_date_competition = REPLACE(pk_date_competition, ' ', '')")

    print('Mise à jour des données de la table Dates_Competions terminée avec succès.')
except Exception as e:
    print(f"Une erreur s'est produite lors de la mise à jour des données : {e}")



try:
    with connection.cursor() as cursor:
        # Mettre à jour pk_date_competition en supprimant les espaces
        cursor.execute("UPDATE my_app_jo_dates_competions SET pk_date_competition = REPLACE(pk_date_competition, ' ', '')")

    print('Mise à jour des données de la table Dates_Competions terminée avec succès.')
except Exception as e:
    print(f"Une erreur s'est produite lors de la mise à jour des données : {e}")


try:
    with connection.cursor() as cursor:
        # Mettre à jour pk_typ_competition en supprimant les espaces
        cursor.execute("UPDATE my_app_jo_competitions SET pk_typ_competition = REPLACE(pk_typ_competition, ' ', '')")

    print('Mise à jour des données de la table Competitions terminée avec succès.')
except Exception as e:
    print(f"Une erreur s'est produite lors de la mise à jour des données : {e}")





try:
    with connection.cursor() as cursor:
        cursor.execute('UPDATE "my_app_jo_offre" SET "pk_Offre" = REPLACE("pk_Offre", \' \', \'\')')

    print('Mise à jour des données de la table Offre terminée avec succès.')
except Exception as e:
    print(f"Une erreur s'est produite lors de la mise à jour des données : {e}")

from my_app_jo.models import Dates_Competions, Competitions
from django.db.models import Value
from django.db.models.functions import Replace

# # Supprimer les virgules, les points-virgules et les espaces de la colonne pk_date_competition
from django.db.models import F, Value
from django.db.models.functions import Replace

# Exécution de la mise à jour
Dates_Competions.objects.update(pk_date_competition=Replace( Replace(Replace( Replace( Replace( Replace(F('pk_date_competition'),
                                                                                                            Value(','),
                                                                                                            Value('')),  
                                                                                                            Value(';'), 
                                                                                                            Value('-')), 
                                                                                                            Value('_')), 
                                                                                                            Value(' ')), 
                                                                                                            Value(',')), 
                                                                                                            Value(''))
)

Competitions.objects.all().update(pk_typ_competition=Replace(Replace(Replace('pk_typ_competition', Value(','), Value('')), Value(';'), Value('')), Value(' '), Value('')))
print("Mise à jour des données terminée avec succès.")
