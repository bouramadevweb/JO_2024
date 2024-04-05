from django.shortcuts import render, redirect, get_object_or_404
from my_app_jo.models import List_competition
from .form import ListCompetitionForm

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
