from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Commande, Competitions, Offre,Code
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,UserChangeForm
from django import forms

class VerificationCodeForm(forms.Form):
    ''' verification du code sms
    '''
    verification_code = forms.CharField(label='Code de vérification', max_length=6)

class BootstrapAuthenticationForm(AuthenticationForm):
    '''authentification 
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mot de passe'})

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class CommandeForm(forms.Form):
    '''
    '''
    quantite = forms.IntegerField(label='Quantité', min_value=1)

class ModifierCommandeForm(forms.ModelForm):
    offre = forms.ModelChoiceField(queryset=Offre.objects.all(), label='pk_Offre')
    quantite = forms.IntegerField(label='Quantité', min_value=1)

    class Meta:
        model = Commande
        fields = ['pk_Offre', 'quantite', 'MontantTotal']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','phone_number')
class PhoneNumberField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', 'Tel : indicatif de votre pays exemple pour la  france = +330255256412')
        kwargs.setdefault('max_length', 12) 
        kwargs.setdefault('widget', forms.TextInput(attrs={'type': 'tel', 'class': 'form-control', 'placeholder': '+33612345678', 'required': True}))
        super().__init__(*args, **kwargs)

class InscriptionForm(UserCreationForm):
    ''' inscription 
    '''
    accept_conditions = forms.BooleanField(label="J'accepte les conditions d'inscription", required=True)
    phone_number = PhoneNumberField()

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email', 'phone_number', 'password1', 'password2', 'accept_conditions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        return phone_number
