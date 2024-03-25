from django import forms
from .models import User,Commande,Competitions,Offre


class CommandeForm(forms.Form):
    quantite = forms.IntegerField(label='Quantité', min_value=1)
class ModifierCommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['pk_Offre', 'quantite', 'MontantTotal']

    offre = forms.ModelChoiceField(queryset=Offre.objects.all(), label='pk_Offre')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Définissez le queryset pour le champ "offre" pour qu'il inclue seulement
        # les offres associées à la compétition de la commande actuelle.
        if self.instance.pk:
            competition_de_la_commande = self.instance.pk_Offre.competition
            self.fields['pk_Offre'].queryset = Offre.objects.filter(competition=competition_de_la_commande)
            
class InscriptionForm(forms.ModelForm):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={
            'min_length': "Le mot de passe est trop court. Il doit comporter au moins %(min_length)d caractères.",
            'password_mismatch': "Les deux mots de passe ne correspondent pas.",
            'numeric_password': "Le mot de passe ne peut pas être entièrement numérique.",
        },
        help_text="Votre mot de passe doit comporter au moins 8 caractères.",
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={
            'password_mismatch': "Les deux mots de passe ne correspondent pas.",
        },
    )
    Date_de_Naissance = forms.DateField(label="Date de Naissance", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'AAAA-MM-JJ'}))
    accept_conditions = forms.BooleanField(label="J'accepte les conditions d'inscription", required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'Date_de_Naissance', 'accept_conditions']