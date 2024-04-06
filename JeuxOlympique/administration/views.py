from django.shortcuts import render, redirect, get_object_or_404
from my_app_jo.models import List_competition,Lieu_des_competions,Dates_Competions
from .form import ListCompetitionForm,LieuDesCompetionsForm,DatesCompetitionsForm

def list_competition(request):
    if request.method == 'POST':
        # Gérer les opérations CRUD
        if 'add' in request.POST:
            form = ListCompetitionForm(request.POST)
            if form.is_valid():
                form.save()
        elif 'update' in request.POST:
            competition_id = request.POST.get('id')
            competition = get_object_or_404(List_competition, pk=competition_id)
            form = ListCompetitionForm(request.POST, instance=competition)
            if form.is_valid():
                form.save()
        elif 'delete' in request.POST:
            competition_id = request.POST.get('id')
            competition = get_object_or_404(List_competition, pk=competition_id)
            competition.delete()
        return redirect('listCompetitions/list_competition')  # Rediriger pour éviter les re-postages
    else:
        list_competition = List_competition.objects.all()
        form = ListCompetitionForm()

        return render(request, 'listCompetitions/list_competition.html', {'list_competition': list_competition, 'form': form})



def lieu_competition(request):
    if request.method == 'POST':
        # Gérer les opérations CRUD
        if 'add' in request.POST:
            form = LieuDesCompetionsForm(request.POST)
            if form.is_valid():
                form.save()
        elif 'update' in request.POST:
            lieu_id = request.POST.get('id')
            lieu = get_object_or_404(Lieu_des_competions, pk=lieu_id)
            form = LieuDesCompetionsForm(request.POST, instance=lieu)
            if form.is_valid():
                form.save()
        elif 'delete' in request.POST:
            lieu_id = request.POST.get('id')
            lieu = get_object_or_404(Lieu_des_competions, pk=lieu_id)
            lieu.delete()
        return redirect('lieux_competitions/lieu_competitions')  # Rediriger pour éviter les re-postages
    else:
        lieu_competition = Lieu_des_competions.objects.all()
        form = LieuDesCompetionsForm()

        return render(request, 'lieux_competitions/lieu_competitions.html', {'lieu_competition': lieu_competition, 'form': form})

def dates_competitions(request):
    if request.method == 'POST':
        # Gérer les opérations CRUD
        if 'add' in request.POST:
            form = DatesCompetitionsForm(request.POST)
            if form.is_valid():
                form.save()
        elif 'update' in request.POST:
            date_competition_id = request.POST.get('id')
            date_competition = get_object_or_404(Dates_Competions, pk=date_competition_id)
            form = DatesCompetitionsForm(request.POST, instance=date_competition)
            if form.is_valid():
                form.save()
        elif 'delete' in request.POST:
            date_competition_id = request.POST.get('id')
            date_competition = get_object_or_404(Dates_Competions, pk=date_competition_id)
            date_competition.delete()
        return redirect('dates_competitions/dates_competitions')  # Rediriger pour éviter les re-postages
    else:
        dates_competitions = Dates_Competions.objects.all()
        form = DatesCompetitionsForm()
        return render(request, 'dates_competitions/dates_competitions.html', {'dates_competitions': dates_competitions, 'form': form})