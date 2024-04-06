from django import forms
from my_app_jo.models import List_competition,Lieu_des_competions,Dates_Competions

class ListCompetitionForm(forms.ModelForm):
    class Meta:
        model = List_competition
        fields = ['nom']

class LieuDesCompetionsForm(forms.ModelForm):
    class Meta:
        model = Lieu_des_competions
        fields = ['Nom', 'Ville', 'Capacite','Discipline']
class DatesCompetitionsForm(forms.ModelForm):
    class Meta:
        model = Dates_Competions
        fields = '__all__' 