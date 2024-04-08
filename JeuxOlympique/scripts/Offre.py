from my_app_jo.models import Offre, Competitions

# Récupérer toutes les compétitions
competitions = Competitions.objects.all()

# Définir les détails des offres
details_offres = {
    'One': {'nombre_personnes': 1, 'prix': 25.5},
    'Duo': {'nombre_personnes': 2, 'prix': 35.5},
    'Famille': {'nombre_personnes': 4, 'prix': 55}
}

# Variable pour suivre le nombre d'offres créées
total_offres_crees = 0

# Parcourir toutes les compétitions
for competition in competitions:
    # Nettoyer la valeur de pk_typ_competition en supprimant les espaces
    pk_typ_competition_cleaned = competition.pk_typ_competition.strip()

    # Parcourir les détails des offres et créer chaque offre
    for offre_type, offre_details in details_offres.items():
        # Nettoyer la valeur de offre_type en supprimant les espaces
        offre_type_cleaned = offre_type.strip()

        # Créer une instance d'Offre avec les détails spécifiés
        offre_pk = f"{pk_typ_competition_cleaned}_{offre_type_cleaned}".replace(" ", "")  # Supprimer les espaces
        offre_instance = Offre(
            pk_Offre=offre_pk,
            type=offre_type_cleaned,
            nombre_personnes=offre_details['nombre_personnes'],
            prix=offre_details['prix'],
            competition=competition
        )
        # Gérer les erreurs potentielles lors de l'enregistrement de l'instance dans la base de données
        try:
            offre_instance.save()
            total_offres_crees += 1
        except Exception as e:
            print(f"Erreur lors de la création de l'offre pour {competition} : {e}")

print(f"Total des offres créées : {total_offres_crees}")
