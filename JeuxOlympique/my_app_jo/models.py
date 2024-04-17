from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import random
import secrets
from django.conf import settings

class User(AbstractUser):
    """_summary_

    Args:
        AbstractUser (_type_): _description_

    Returns: User
        
    """
    Nom = models.CharField(max_length=150)
    Prenom = models.CharField(max_length=150)
    ClefGeneree = models.CharField(max_length=50, default=secrets.token_hex(16))
    phone_number = models.CharField(max_length=12)

    class Meta:
        db_table = 'auth_user'
        swappable = 'AUTH_USER_MODEL'
        default_permissions = ()
        permissions = (('create_users', 'Can create users'),)
        abstract = False
    

    def __str__(self):
        return f'{self.Nom}, {self.Prenom}'
class Code(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns: Code pour identification
        
    """
    number = models.CharField(max_length=5, blank=True, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    est_validee = models.BooleanField(default=False)
    last_generated = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return str(self.number)

    def save(self, *args, **kwargs):
        if not self.number or 'force_insert' in kwargs:  
            while True:
                number_list = [x for x in range(10)]
                code_items = []
                for _ in range(5):
                    num = random.choice(number_list)
                    code_items.append(str(num))
                new_code = "".join(code_items)
                
                if not Code.objects.filter(number=new_code).exists():
                    self.number = new_code
                    break  
        
        super().save(*args, **kwargs)
    def verifier(self):
        # Fonction pour vérifier le code et mettre à jour est_validee
        self.est_validee = True
        self.save()    

def get_List_competition_image_path(instance, filename):
    # Définir le chemin de téléversement en fonction de l'ID de l'instance
    folder_name = str(instance.pk_list_competition)
    return f'List_competition_images/{folder_name}/{filename}'

class List_competition(models.Model):
    """_summary_

    Args:
        models (_type_):List des competitions

    Returns: la liste des Competition
        
    """
    pk_list_competition = models.CharField(max_length=150, primary_key=True ,unique=True)
    nom = models.CharField(max_length=150)
    image = models.ImageField(upload_to=get_List_competition_image_path, null=True, blank=True)
    
    def get_List_competition_image_path(instance, filename):
           return f'List_competition_images/{instance.pk_list_competition}/{filename}'

   
    def __str__(self):
        return f'{self.pk_list_competition}, {self.nom}'


class Lieu_des_competions(models.Model):
    """_summary_

    Args:
        models (_type_): Lieux des competitions

    Returns: lieux des Competitions
        
    """
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
            
            self.pk_lieu = "_".join([str(self.Ville),str(self.Nom.strip()),str(self.Capacite),str(self.Discipline.pk_list_competition.strip())]).replace(',', '').replace(';', '').replace(' ', '').replace('-', '')
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.Nom}, {self.Ville}, {self.Capacite} ,{self.Discipline.nom}'    
class Dates_Competions(models.Model):
    """_summary_

    Args:
        models (_type_): dates des Competitions

    Returns: date des competitions

    """
    # Définir le champ pour la clé primaire concaténée
    pk_date_competition = models.CharField(max_length=600, primary_key=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    pk_list_competition = models.ForeignKey(List_competition, on_delete=models.CASCADE)
    pk_lieu = models.ForeignKey(Lieu_des_competions, on_delete=models.CASCADE)
    Remises_de_medailles = models.CharField(max_length=250, default='')  # Valeur par défaut ajoutée ici

    def save(self, *args, **kwargs):
        # Concaténer les champs pour former la clé primaire
        self.pk_date_competition = "_".join([str(self.pk_list_competition.pk_list_competition),
                                             str(self.pk_lieu.pk_lieu),str(self.date_debut),
                                             str(self.date_fin),
                                             str(self.Remises_de_medailles)]).replace(',', '').replace(';', '').replace(' ', '').replace('-', '')
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.pk_date_competition},{self.date_debut} ,{self.date_fin},{self.Remises_de_medailles}'


def get_competition_image_path(instance, filename):
    folder_name = instance.Nom
    return f'competition_images/{folder_name}/{filename}'

class Competitions(models.Model):
    """_summary_

    Args:
        models (_type_): les Competitions

    Returns: les Competitions
    """
    pk_typ_competition = models.CharField(max_length=1000, primary_key=True)
    Nom = models.CharField(max_length=250)
    pk_list_competition = models.ForeignKey(List_competition, on_delete=models.CASCADE)
    pk_date_competition = models.ForeignKey(Dates_Competions, on_delete=models.CASCADE)
    pk_lieu = models.ForeignKey(Lieu_des_competions, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_competition_image_path, null=True, blank=True, max_length=455)

    def save(self, *args, **kwargs):
        # Vérifier si les clés étrangères ne sont pas nulles
        if self.pk_lieu_id is not None and self.pk_list_competition_id is not None:
            # Former la clé primaire en utilisant les instances des objets associés
            self.pk_typ_competition = f"{self.pk_list_competition.pk_list_competition}_{self.pk_date_competition.pk_date_competition}_{self.pk_lieu.pk_lieu}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.Nom
    
class Types(models.Model):
    """_summary_

    Args:
        models (_type_): Types Offre

    Returns: Type Offre
        
    """
    type =models.CharField(primary_key=True)
    def __str__(self):
        return f'{self.type}'

class Offre(models.Model):
    """_summary_

    Args:
        models (_type_): Offre

    Returns: Offre
    """
   
    pk_Offre = models.CharField(max_length=2000, primary_key=True)
    type = models.ForeignKey(Types, on_delete=models.CASCADE)
    nombre_personnes = models.IntegerField()
    prix = models.FloatField()
    competition = models.ForeignKey(Competitions, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk_Offre:
            self.pk_Offre = "_".join([str(self.type), str(self.nombre_personnes), str(self.competition.pk_list_competition)]).replace(',', '').replace(';', '').replace(' ', '')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.pk_Offre}, {self.type}, {self.prix}, {self.competition.Nom}'
    
class Billet(models.Model):
    """_summary_

    Args:
        models (_type_):Billet

    Returns: Billet Electronique
    """
    pk_Billet = models.AutoField(primary_key=True)
    Cledebilletelectroniquesecurisee = models.CharField(max_length=50, unique=True)
    ClefUtilisateur = models.CharField(max_length=50)
    pk_typ_competition = models.ForeignKey('Competitions', on_delete=models.CASCADE)
    est_validee = models.BooleanField(default=False)
    date_dachat = models.DateField(auto_now_add=True)
    date_valide = models.DateField(null =True)
    
    def save(self, *args, **kwargs):
        if not self.pk_Billet:
            # Générer une clé unique sécurisée
            self.Cledebilletelectroniquesecurisee = uuid.uuid4().hex
        super().save(*args, **kwargs)

    
    
    def __str__(self):
        return f'Billet {self.pk_Billet} pour {self.pk_typ_competition}'

class Commande(models.Model):
    """_summary_

    Args:
        models (_type_): Commande

    Returns: Les commandes 
    """
    pk_Commande = models.AutoField(primary_key=True)
    quantite = models.IntegerField()
    MontantTotal = models.FloatField()
    pk_date = models.DateTimeField(auto_now_add=True)
    pk_Offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    pk_Utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pk_Billet = models.ForeignKey(Billet, on_delete=models.CASCADE)
    est_validee = models.BooleanField(default=False)
    def __str__(self):
        return f'Commande {self.pk_Commande} pour {self.quantite} billet(s) {self.pk_Offre.type}'

    def save(self, *args, **kwargs):
        if not self.pk_Billet_id:
            billet = Billet.objects.create(
                pk_typ_competition=self.pk_Offre.competition,
                date_valide=self.pk_Offre.competition.pk_date_competition.date_debut
            )
            billet.ClefUtilisateur = self.pk_Utilisateur.ClefGeneree
            billet.save()
            self.pk_Billet = billet
        super().save(*args, **kwargs)

 
class ODS(models.Model):
    """_summary_

    Args:
        models (_type_):ODS  ou entrepôt de données opérationnelles en français
    """
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


