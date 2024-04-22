from my_app_jo.models import Offre, Competitions, Types

def creer_offres():
    # Récupérer toutes les compétitions existantes
    competitions = Competitions.objects.all()

    # Récupérer tous les types d'offres disponibles
    types_offres = Types.objects.all()

    # Définir les détails des offres pour chaque type
    offres_details = {
        'One': {'nombre_personnes': 1, 'prix': 25.5},
        'Duo': {'nombre_personnes': 2, 'prix': 35.5},
        'Famille': {'nombre_personnes': 4, 'prix': 55}
    }

    # Variable pour suivre le nombre d'offres créées
    total_offres_crees = 0

    # Parcourir toutes les compétitions
    for competition in competitions:
        # Parcourir tous les types d'offres
        for type_offre in types_offres:
            # Récupérer les détails de l'offre pour ce type à partir du dictionnaire offres_details
            offre_details = offres_details.get(type_offre.type)

            # Si les détails de l'offre sont trouvés, créer une instance d'Offre
            if offre_details:
                # Créer une instance d'Offre avec les détails spécifiés
                offre_pk = f"{competition.pk_typ_competition}_{type_offre.type}".replace(" ", "")  # Supprimer les espaces
                offre_instance = Offre(
                    pk_Offre=offre_pk,
                    type=type_offre,
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

# Exécuter la fonction pour créer les offres
creer_offres()
