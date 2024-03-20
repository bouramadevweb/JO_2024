from django.db import models
from django.contrib.auth.models import User

import secrets
import string

class Offre(models.Model):
    pk_Offre = models.CharField(max_length=50, primary_key=True)
    Type = models.CharField(max_length=250)
    NombrePersonnes = models.IntegerField()
    Prix = models.FloatField()

    def __str__(self):
        return f'{self.pk_Offre}, {self.Type}, {self.Prix}'

class Utilisateur(models.Model):
    pk_Utilisateur = models.AutoField(primary_key=True)
    Nom = models.CharField(max_length=150)
    Prenom = models.CharField(max_length=150)
    AdresseEmail = models.EmailField(max_length=50, unique=True)
    MotDePasse = models.CharField(max_length=250)
    Date_de_Naissance = models.DateField()
    ClefGeneree = models.CharField(max_length=50, default=secrets.token_hex(16))

    def __str__(self):
        return f'{self.Nom}, {self.Prenom}, {self.AdresseEmail}'


class Dates_commandes(models.Model):
    pk_date = models.DateTimeField(primary_key=True)

    def __str__(self):
        return f'{self.pk_date}'

class List_competition(models.Model):
    pk_list_competition = models.CharField(max_length=150, primary_key=True)

    def __str__(self):
        return f'{self.pk_list_competition}'
class Lieu_des_competions(models.Model):
    pk_lieu = models.AutoField(primary_key=True)
    Nom = models.CharField(max_length=250)
    Ville = models.CharField(max_length=50)
    Capacite = models.BigIntegerField()
    Discipline = models.ForeignKey(List_competition, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.Nom}, {self.Ville}, {self.Capacite}'    
class Dates_Competions(models.Model):
    # Définir le champ pour la clé primaire concaténée
    pk_date_competition = models.CharField(max_length=255, primary_key=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    pk_list_competition = models.ForeignKey(List_competition, on_delete=models.CASCADE)
    Remises_de_medailles = models.CharField(max_length=250, default='')  # Valeur par défaut ajoutée ici

    def save(self, *args, **kwargs):
        # Concaténer les champs pour former la clé primaire
        self.pk_date_competition = f"{self.pk_list_competition}_{self.date_debut}_{self.date_fin}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.pk_date_competition}, ({self.date_debut} au {self.date_fin}), {self.Remises_de_medailles}'


class Competitions(models.Model):
    pk_typ_competition = models.AutoField(primary_key=True)
    Nom = models.CharField(max_length=250)
    pk_list_competition = models.ForeignKey(List_competition, on_delete=models.CASCADE)
    pk_date_competition = models.ForeignKey(Dates_Competions, on_delete=models.CASCADE)
    pk_lieu = models.ForeignKey(Lieu_des_competions, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.Nom}, {self.pk_list_competition}, {self.pk_date_competition}, {self.pk_lieu}'

class Billet(models.Model):
    pk_Billet = models.AutoField(primary_key=True)
    Cledebilletelectroniquesecurisee = models.CharField(max_length=50)
    ClefBillet = models.CharField(max_length=250)
    ClefSecurite = models.CharField(max_length=250)
    pk_typ_competition = models.ForeignKey(Competitions, on_delete=models.CASCADE)

    def __str__(self):
        return f'Billet {self.pk_Billet} pour {self.pk_typ_competition}'

    def generer_cle(self):
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for i in range(20))

class Commande(models.Model):
    pk_Commande = models.AutoField(primary_key=True)
    quantite = models.IntegerField()
    MontantTotal = models.FloatField()
    pk_date = models.DateTimeField(auto_now_add=True)
    pk_Offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    pk_Utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    pk_Billet = models.ForeignKey(Billet, on_delete=models.CASCADE)
    pk_Competition = models.ForeignKey(Competitions, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'Commande {self.pk_Commande} pour {self.quantite} billet(s)'

    def save(self, *args, **kwargs):
        if not self.pk_Billet:
            billet = Billet.objects.create(pk_typ_competition=self.pk_Competition)
            billet.Cledebilletelectroniquesecurisee = billet.generer_cle()
            billet.save()
            self.pk_Billet = billet
        super(Commande, self).save(*args, **kwargs)

class ODS(models.Model):
    discipline = models.CharField(max_length=250)
    date_debut = models.DateField()
    date_fin = models.DateField()
    lieu = models.CharField(max_length=250)
    capacite = models.BigIntegerField()
    remises_de_medailles = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return f'{self.discipline} - {self.lieu} ({self.date_debut} to {self.date_fin})'
