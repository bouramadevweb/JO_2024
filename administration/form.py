from dataclasses import field
from django import forms
from my_app_jo.models import List_competition,Lieu_des_competions,Dates_Competions,Competitions,Offre,Commande, Types
from django.contrib.auth.forms import UserCreationForm
from my_app_jo.models import User
from django.contrib.auth.forms import AuthenticationForm

from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserChangeForm

class CustomUserChangeForms(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','phone_number')
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}))

class BootstrapAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mot de passe'})
        
class AdminInscriptionForm(UserCreationForm):
    accept_conditions = forms.BooleanField(label="J'accepte les conditions d'inscription", required=True)
    is_superuser = forms.BooleanField(label="Administrateur", required=True)
    phone_number = forms.CharField(label="Numéro de téléphone", max_length=12)

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email', 'phone_number', 'password1', 'password2','is_superuser']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_superuser'].widget.attrs.update({'class': 'form-control'})

class InscriptionForm(UserCreationForm):
    accept_conditions = forms.BooleanField(label="J'accepte les conditions d'inscription", required=True)
    phone_number = forms.CharField(max_length=12)

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email', 'phone_number', 'password1', 'password2','is_superuser']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_superuser'].widget.attrs.update({'class': 'form-control'})
        
class ListCompetitionForm(forms.ModelForm):
    class Meta:
        model = List_competition
        fields = ['nom', 'image']

class LieuDesCompetionsForm(forms.ModelForm):
    class Meta:
        model = Lieu_des_competions
        fields = ['Nom', 'Ville', 'Capacite','Discipline']

class DatesCompetitionsForm(forms.ModelForm):
    class Meta:
        model = Dates_Competions
        fields = '__all__' 


class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competitions
        fields = ['Nom']
class TypesForm(forms.ModelForm):
    class Meta:
       model= Types
       fields= ['type']

class OffreForm(forms.ModelForm):
    
    class Meta:
        model = Offre
        fields = [ 'type','nombre_personnes', 'prix', 'competition']

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['quantite', 'MontantTotal', 'pk_Offre', 'pk_Utilisateur', 'pk_Billet', 'est_validee']
