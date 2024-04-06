from django import forms
from my_app_jo.models import List_competition,Lieu_des_competions,Dates_Competions,Competitions

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

# class CompetitionForm(forms.ModelForm):
#     class Meta:
#         model = Competitions
#         fields = ['Nom','pk_list_competition', 'pk_date_competition', 'pk_lieu']
#         labels = {
#             'Nom': 'Nom de la compétition',
#             'pk_date_competition': 'Date de la compétition',
#             'pk_lieu': 'Lieu de la compétition'
#         }
#         widgets = {
#             'pk_date_competition': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'pk_lieu': forms.TextInput(attrs={'class': 'form-control'}),
        # }

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competitions
        fields = ['Nom']
