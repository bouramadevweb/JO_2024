from django.db import models
from django.contrib.auth.models import AbstractUser

import secrets
import string
from django.conf import settings

class User(AbstractUser):
    Nom = models.CharField(max_length=150)
    Prenom = models.CharField(max_length=150)
    AdresseEmail = models.EmailField(max_length=50, unique=True)
    Date_de_Naissance = models.DateField()
    ClefGeneree = models.CharField(max_length=50, default=secrets.token_hex(16))

    class Meta:
        db_table = 'auth_user'
        swappable = 'AUTH_USER_MODEL'
        default_permissions = ()
        permissions = (('create_users', 'Can create users'),)
        abstract = False

    def __str__(self):
        return f'{self.Nom}, {self.Prenom}, {self.AdresseEmail}'

class Dates_commandes(models.Model):
    pk_date = models.DateTimeField(primary_key=True)

    def __str__(self):
        return f'{self.pk_date}'

class List_competition(models.Model):
    pk_list_competition = models.CharField(max_length=150, primary_key=True)
    nom =models.CharField(max_length=150)

    def __str__(self):
        return f'{self.pk_list_competition} ,{self.nom}'

class Lieu_des_competions(models.Model):
    # Définir le champ pour la clé primaire AutoField
    pk_lieu = models.CharField(max_length=250,primary_key=True)
    Nom = models.CharField(max_length=250)
    Ville = models.CharField(max_length=50)
    Capacite = models.BigIntegerField()
    Discipline = models.ForeignKey(List_competition, on_delete=models.CASCADE)
    def diminuer_capacite(self, quantite):
        """
        Diminue la capacité du lieu lorsqu'une commande est passée.
        """
        self.Capacite -= quantite
        self.save()
    def save(self, *args, **kwargs):
        # Si l'objet n'a pas encore de clé primaire, créez-en une en utilisant les valeurs des champs spécifiés
        if not self.pk:
            self.pk_lieu = f"{self.Ville}_{self.Nom}_{self.Capacite}_{self.Discipline.pk_list_competition}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.Nom}, {self.Ville}, {self.Capacite}'    
class Dates_Competions(models.Model):
    # Définir le champ pour la clé primaire concaténée
    pk_date_competition = models.CharField(max_length=255, primary_key=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    pk_list_competition = models.ForeignKey(List_competition, on_delete=models.CASCADE)
    pk_lieu = models.ForeignKey(Lieu_des_competions, on_delete=models.CASCADE)
    Remises_de_medailles = models.CharField(max_length=250, default='')  # Valeur par défaut ajoutée ici

    def save(self, *args, **kwargs):
        # Concaténer les champs pour former la clé primaire
        self.pk_date_competition = f"{self.pk_list_competition}_{self.pk_lieu}_{self.date_debut}_{self.date_fin}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.pk_date_competition},{self.date_debut} ,{self.date_fin},{self.Remises_de_medailles}'


class Competitions(models.Model):
    pk_typ_competition = models.CharField(primary_key=True)
    Nom = models.CharField(max_length=250)
    pk_list_competition = models.ForeignKey(List_competition, on_delete=models.CASCADE)
    pk_date_competition = models.ForeignKey(Dates_Competions, on_delete=models.CASCADE)
    pk_lieu = models.ForeignKey(Lieu_des_competions, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        # Concaténer les champs pour former la clé primaire
        self.pk_typ_competition = f"{self.pk_lieu}{self.pk_list_competition}_{self.pk_date_competition}"
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.Nom}, {self.pk_typ_competition}, {self.pk_date_competition}, {self.pk_lieu}'
    
class Offre(models.Model):
    TYPE_CHOICES = [
        ('One', 'One'),
        ('Duo', 'Duo'),
        ('Famille', 'Famille'),
    ]

    pk_Offre = models.CharField(max_length=2000, primary_key=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    nombre_personnes = models.IntegerField()
    prix = models.FloatField()
    competition = models.ForeignKey(Competitions, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk_Offre}, {self.type}, {self.prix}, {self.competition.Nom}'


class Billet(models.Model):
    pk_Billet = models.AutoField(primary_key=True)
    Cledebilletelectroniquesecurisee = models.CharField(max_length=50, unique=True)  # Clé de sécurité générée lors de la création du billet électronique
    ClefUtilisateur = models.CharField(max_length=50)  # Clé associée à l'utilisateur pour sécuriser le billet
    pk_typ_competition = models.ForeignKey(Competitions, on_delete=models.CASCADE)

    def __str__(self):
        return f'Billet {self.pk_Billet} pour {self.pk_typ_competition}'

    def generer_cles(self):
        """
        Génère les clés de sécurité pour le billet électronique.
        """
        self.Cledebilletelectroniquesecurisee = self.generer_cle()
        self.ClefUtilisateur = self.pk_typ_competition.pk_Utilisateur.ClefGeneree
        self.save()

    def generer_cle(self):
        """
        Génère une clé de sécurité aléatoire.
        """
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for i in range(20))


class Commande(models.Model):
    pk_Commande = models.AutoField(primary_key=True)
    quantite = models.IntegerField()
    MontantTotal = models.FloatField()
    pk_date = models.DateTimeField(auto_now_add=True)
    pk_Offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    # Mettez à jour le champ pk_Utilisateur pour utiliser le modèle utilisateur personnalisé
    pk_Utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Utilisez le modèle utilisateur personnalisé
    pk_Billet = models.ForeignKey(Billet, on_delete=models.CASCADE)

    def __str__(self):
        return f'Commande {self.pk_Commande} pour {self.quantite} billet(s)'

    def save(self, *args, **kwargs):
        if not self.pk_Billet_id:
            billet = Billet.objects.create(pk_typ_competition=self.pk_Competition)
            billet.Cledebilletelectroniquesecurisee = billet.generer_cle()
            billet.ClefUtilisateur = self.pk_Utilisateur.clefgeneree
            billet.save()
            self.pk_Billet = billet
        super().save(*args, **kwargs)

class ODS(models.Model):
    discipline = models.CharField(max_length=250)
    date_debut = models.DateField()
    date_fin = models.DateField()
    lieu = models.CharField(max_length=250)
    ville = models.CharField(max_length=250)
    capacite = models.TextField()  # Utilisez un TextField pour stocker les listes
    remises_de_medailles = models.CharField(max_length=250, blank=True)

    def save(self, *args, **kwargs):
        # Convertir la capacité en chaîne de caractères avant de sauvegarder
        if isinstance(self.capacite, list):
            self.capacite = str(self.capacite)
        super().save(*args, **kwargs)