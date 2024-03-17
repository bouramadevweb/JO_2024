# Dans le fichier models.py de l'application olympics

from django.db import models
from django.contrib.auth.models import User
import uuid

class Offre(models.Model):
    pk_offre =models.CharField(primary_key=True)
    Type = models.CharField(max_length=250)
    NombrePersonnes = models.IntegerField()
    Prix = models.FloatField()

class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ClefGeneree = models.UUIDField(default=uuid.uuid4, editable=False)
    Date_de_Naissance = models.DateField()

class LieuDesCompetitions(models.Model):
    Nom = models.CharField(max_length=250, unique=True)
    Ville = models.CharField(max_length=50)
    Capacite = models.BigIntegerField()

class DatesCommandes(models.Model):
    pk_date = models.DateTimeField(primary_key=True)

class DatesCompetitions(models.Model):
    pk_date_competition = models.DateTimeField(primary_key=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    def __str__(self):
        return self.pk_date_competition +self.date_debut + self.date_fin

class ListCompetition(models.Model):
    pk_list_competition = models.CharField(max_length=50, primary_key=True)
    def __str__(self):
        return self.pk_list_competition

class Competition(models.Model):
    pk_competition =models.CharField(primary_key=True)
    Nom = models.CharField(max_length=250)
    pk_list_competition = models.ForeignKey(ListCompetition, on_delete=models.CASCADE)
    pk_date_competition = models.ForeignKey(DatesCompetitions, on_delete=models.CASCADE)
    pk_lieu = models.ForeignKey(LieuDesCompetitions, on_delete=models.CASCADE)

class Billet(models.Model):
    ClefBillet = models.CharField(max_length=250)
    ClefSecurite = models.CharField(max_length=250)
    pk_typ_competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

class Commande(models.Model):
    quantite = models.IntegerField()
    MontantTotal = models.FloatField()
    pk_date = models.ForeignKey(DatesCommandes, on_delete=models.CASCADE)
    pk_offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    pk_utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    pk_billet = models.ForeignKey(Billet, on_delete=models.CASCADE)
