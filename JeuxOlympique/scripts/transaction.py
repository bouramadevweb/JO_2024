from my_app_jo.models import ODS, Lieu_des_competions, List_competition, Dates_Competions, Offre, Competitions
from django.db import IntegrityError, transaction

def remove_spaces(text):
    return text.replace(' ', '')

def run():
    try:
        # Section 1 : Insertion des données pour les lieux de compétitions
        with transaction.atomic():
            for competition_entry in ODS.objects.all():
                print(f"Insertion des données pour {competition_entry.discipline}")

                if competition_entry.discipline:
                    try:
                        discipline_instance = List_competition.objects.get(pk_list_competition=competition_entry.discipline.strip())
                    except List_competition.DoesNotExist:
                        discipline_instance = List_competition.objects.create(
                            pk_list_competition=competition_entry.discipline.strip(),
                            nom=competition_entry.discipline
                        )

                    pk_lieu = competition_entry.lieu.replace(' ', '')

                    lieu_competition = Lieu_des_competions(
                        pk_lieu=pk_lieu,
                        Nom=competition_entry.lieu,
                        Discipline=discipline_instance,
                        Capacite=competition_entry.capacite,
                        Ville=competition_entry.ville
                    )
                    lieu_competition.save()

            print("Fin d'insertion des données pour les lieux de compétitions")

        # Section 2 : Insertion des données pour les dates de compétitions
        with transaction.atomic():
            for ods_entry in ODS.objects.all():
                try:
                    list_competition_instance = List_competition.objects.get(pk_list_competition=ods_entry.discipline.strip())
                except List_competition.DoesNotExist:
                    print(f"La discipline '{ods_entry.discipline}' de l'ODS n'existe pas dans la table List_competition.")
                    continue

                lieu_competition_instances = Lieu_des_competions.objects.filter(Nom=ods_entry.lieu)

                if lieu_competition_instances.exists():
                    print(f"Attention : Plusieurs lieux portent le nom '{ods_entry.lieu}' dans la table Lieu_des_competions.")

                for lieu_competition_instance in lieu_competition_instances:
                    pk_date_competition = f"{lieu_competition_instance.pk_lieu}{ods_entry.date_debut}{ods_entry.date_fin}".replace(' ', '')
                    date_competition = Dates_Competions(
                        pk_date_competition=pk_date_competition,
                        date_debut=ods_entry.date_debut,
                        date_fin=ods_entry.date_fin,
                        pk_list_competition=list_competition_instance,
                        Remises_de_medailles=ods_entry.remises_de_medailles,
                        pk_lieu=lieu_competition_instance
                    )

                    date_competition.save()

            print("Toutes les données ont été insérées avec succès.")

        # Section 3 : Insertion des offres liées aux compétitions
        with transaction.atomic():
            competitions = Competitions.objects.all()
            details_offres = {
                'One': {'nombre_personnes': 1, 'prix': 25.5},
                'Duo': {'nombre_personnes': 2, 'prix': 35.5},
                'Famille': {'nombre_personnes': 4, 'prix': 55}
            }
            total_offres_crees = 0

            for competition in competitions:
                pk_typ_competition_cleaned = competition.pk_typ_competition.strip()

                for offre_type, offre_details in details_offres.items():
                    offre_type_cleaned = offre_type.strip()
                    pk_Offre = f"{pk_typ_competition_cleaned}_{offre_type_cleaned}".replace(" ", "")
                    offre_instance = Offre(
                        pk_Offre=pk_Offre,
                        type=offre_type_cleaned,
                        nombre_personnes=offre_details['nombre_personnes'],
                        prix=offre_details['prix'],
                        competition=competition
                    )
                    offre_instance.save()
                    total_offres_crees += 1

            print(f"Total des offres créées : {total_offres_crees}")

    except IntegrityError as e:
        print(f"IntegrityError: {e}")

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

# Exécuter la méthode run
if __name__ == "__main__":
    run()
