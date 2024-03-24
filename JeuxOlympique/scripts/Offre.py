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
    print("pk_typ_competition_cleaned:", pk_typ_competition_cleaned)

    # Parcourir les détails des offres et créer chaque offre
    for offre_type, offre_details in details_offres.items():
        # Nettoyer la valeur de offre_type en supprimant les espaces
        offre_type_cleaned = offre_type.strip()
        print("offre_type_cleaned:", offre_type_cleaned)

        # Créer une instance d'Offre avec les détails spécifiés
        pk_Offre = f"{pk_typ_competition_cleaned}_{offre_type_cleaned}"
        print("pk_Offre:", pk_Offre)
        offre_instance = Offre(
            pk_Offre=pk_Offre,
            type=offre_type_cleaned,
            nombre_personnes=offre_details['nombre_personnes'],
            prix=offre_details['prix'],
            competition=competition
        )
        # Enregistrer l'instance dans la base de données
        offre_instance.save()
        total_offres_crees += 1
        print(f"Offre créée pour la compétition {competition.Nom} : {offre_type}")

print(f"Total des offres créées : {total_offres_crees}")
