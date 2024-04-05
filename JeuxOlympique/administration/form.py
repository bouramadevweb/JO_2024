from django import forms
from my_app_jo.models import List_competition

class ListCompetitionForm(forms.ModelForm):
    class Meta:
        model = List_competition
        fields = ['nom']