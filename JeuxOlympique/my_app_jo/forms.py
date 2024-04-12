from dataclasses import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Commande, Competitions, Offre,Code
from django.contrib.auth.forms import AuthenticationForm

# class VerificationCodeForm(forms.Form):
#         verification_code = forms.CharField(label='Code de vérification', max_length=6, help_text='Entrez votre code de vérification')
#         model = Code
#         fields =('number')
class VerificationCodeForm(forms.Form):
    verification_code = forms.CharField(label='Code de vérification', max_length=6)

class BootstrapAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mot de passe'})
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class CommandeForm(forms.Form):
    quantite = forms.IntegerField(label='Quantité', min_value=1)

class ModifierCommandeForm(forms.ModelForm):
    offre = forms.ModelChoiceField(queryset=Offre.objects.all(), label='pk_Offre')
    quantite = forms.IntegerField(label='Quantité', min_value=1)

    class Meta:
        model = Commande
        fields = ['pk_Offre', 'quantite', 'MontantTotal']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class InscriptionForm(UserCreationForm):
    accept_conditions = forms.BooleanField(label="J'accepte les conditions d'inscription", required=True)

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email','phone_number' , 'password1', 'password2', 'accept_conditions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})

        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
