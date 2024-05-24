from django.shortcuts import render, redirect, get_object_or_404
from my_app_jo.models import List_competition, Lieu_des_competions, Dates_Competions,Competitions,Offre,Commande,Types,User
from administration.form import TypesForm,ListCompetitionForm, LieuDesCompetionsForm, DatesCompetitionsForm,CompetitionForm,CommandeForm,OffreForm
from django.http import HttpResponse
from django.db.models import Value
from django.db.models.functions import Replace
from django.core.paginator import Paginator
from django.db.models import Count, Sum,Q
from django.contrib.auth.models import User
from my_app_jo.models import User as Users
from django.views.generic import  DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .form import AdminInscriptionForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import AuthenticationForm
from .form import CustomAuthenticationForm,BootstrapAuthenticationForm
from django.contrib.auth import authenticate, login as auth_login  
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout



"""Gestion administration de ce sites ici """


def login(request):
    """admin login
    """
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)  
                return redirect('administration')  
    else:
        form = BootstrapAuthenticationForm()
    return render(request, 'admin/login.html', {'form': form})

def admindeconnexion(request):
    """la deconnexion
    """
    logout(request)
    return redirect('login')

@user_passes_test(lambda u: u.is_superuser, login_url='/administration/login')
def users(request):
    """users
    """
    if request.method == 'GET':
        users = Users.objects.all() 
        paginator = Paginator(users, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        form = UserCreationForm()
        return render(request, 'admin/users.html', {'page_obj': page_obj, 'form': form})

    elif request.method == 'POST':
        if 'add' in request.POST:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('admin/users')
        elif 'update' in request.POST:
            user_id = request.POST.get('id')
            user = get_object_or_404(User, pk=user_id)
            form = UserChangeForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('admin/users')
        elif 'delete' in request.POST:
            user_id = request.POST.get('id')
            user = get_object_or_404(User, pk=user_id)
            user.delete()
            return redirect('admin/users')
        
class AdminCreateView(CreateView):
    form_class = AdminInscriptionForm
    template_name = 'admin/user_form.html'  
    success_url = reverse_lazy('admin_dashboard')
    @user_passes_test(lambda u: u.is_superuser, login_url='/administration/login/')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



def clean_primary_key(value):
    return Replace(Replace(Replace(value, Value(','), Value('')), Value(';'), Value('')), Value('.'), Value(''))

@user_passes_test(lambda u: u.is_superuser, login_url='/administration/login/')
def administration(request):
    """administration 
    """
    return render(request, 'status.html')

@user_passes_test(lambda u: u.is_superuser, login_url='/administration/login/')
def ventes_par_offre(request):
    """Vente par offres
    """
    # Récupérer les offres avec le nombre de ventes pour chaque offre
    ventes_par_offre = Offre.objects.annotate(
        nombre_ventes=Count('commande', filter=Q(commande__est_validee=True)),
        quantite_vendue=Sum('commande__quantite', filter=Q(commande__est_validee=True))
    ).filter(
        commande__est_validee=True  #
    ).annotate(
        montant_total_ventes=Sum('commande__MontantTotal')  # Calcul du montant total des ventes pour chaque offre
    )
     
    
    return render(request, 'commandes/ventes_par_offre.html', {'ventes_par_offre': ventes_par_offre})

    
@user_passes_test(lambda u: u.is_superuser, login_url='/administration/login/')
def list_competition(request):
    """ list des competion
    """
    if request.method == 'GET':
        list_competition = List_competition.objects.all()
        paginator = Paginator(list_competition,10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        form = ListCompetitionForm()
        return render(request, 'listCompetitions/list_competition.html', {'page_obj': page_obj, 'form': form})

    elif request.method == 'POST':
        if 'add' in request.POST:
            form = ListCompetitionForm(request.POST, request.FILES)  # Ajouter request.FILES pour traiter les fichiers
            if form.is_valid():
                form.save()
        elif 'update' in request.POST:
            competition_id = request.POST.get('id')
            competition = get_object_or_404(List_competition, pk=competition_id)
            form = ListCompetitionForm(request.POST, request.FILES, instance=competition)  # Ajouter request.FILES
            if form.is_valid():
                form.save()
                return redirect('list_competition')
        elif 'delete' in request.POST:
            competition_id = request.POST.get('id')
            competition = get_object_or_404(List_competition, pk=competition_id)
            competition.delete()
        return redirect('list_competition')
    
@user_passes_test(lambda u: u.is_superuser, login_url='/administration/login/')
def upload_image(request):
    """ gestion insertion image pour competitions
    """
    if request.method == 'POST':
        competition_id = request.POST.get('competition')
        try:
            competition = Competitions.objects.get(pk_typ_competition=competition_id)
        except Competitions.DoesNotExist:
            return HttpResponse('Compétition non trouvée.')
        
        image_file = request.FILES.get('image')
        
        # Enregistrez l'image pour la compétition sélectionnée
        if image_file and competition:
            competition.image = image_file
            competition.save()
            return HttpResponse('Image ajoutée avec succès à la compétition {}'.format(competition.Nom))
    
    # Récupérer toutes les compétitions pour afficher dans le formulaire déroulant
    competitions = Competitions.objects.all()
    
    # Rendre le template HTML avec le contexte des compétitions
    return render(request, 'competitions/upload_image.html', {'competitions': competitions})

@user_passes_test(lambda u: u.is_superuser, login_url='/administration/login/')
def lieu_competition(request):
    """Lieu Competion
    """
    if request.method == 'GET':
        lieu_competition = Lieu_des_competions.objects.all()
        paginator = Paginator(lieu_competition,10)  # Paginer par 10 éléments par page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        form = LieuDesCompetionsForm()
        return render(request, 'lieux_competitions/lieu_competitions.html', {'page_obj': page_obj, 'form': form})

    elif request.method == 'POST':
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
        return redirect('lieu_competition')
    
@user_passes_test(lambda u: u.is_superuser, login_url='/administration/login/')
def dates_competitions(request):
    """Dates Competitions
    """
    if request.method == 'GET':
        dates_competitions = Dates_Competions.objects.all().annotate(
            cleaned_pk_date_competition=clean_primary_key('pk_date_competition')
        )
        paginator =Paginator(dates_competitions,10)
        page_number = request.GET.get('page')
        page_obj  = paginator.get_page(page_number)
        form = DatesCompetitionsForm()
        return render(request, 'dates_competitions/dates_competitions.html', {'page_obj': page_obj, 'form': form})

    elif request.method == 'POST':
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
                return redirect('dates_competitions/dates_competitions')
        elif 'delete' in request.POST:
            date_competition_id = request.POST.get('id')
            date_competition = get_object_or_404(Dates_Competions, pk=date_competition_id)
            date_competition.delete()
        return redirect('dates_competitions/dates_competitions')  # Rediriger pour éviter les re-postages
    

@user_passes_test(lambda u: u.is_superuser, login_url='/administration/login/')
def competitions(request):
    """Competitions
    """
    if request.method == 'GET':
        competitions = Competitions.objects.all()
        paginator =Paginator(competitions,10)
        page_number =request.GET.get ('page')
        page_obj = paginator.get_page(page_number)
        form = CompetitionForm()
        return render(request, 'competitions/competitions.html', {'page_obj': page_obj, 'form': form})
    elif request.method == 'POST':
        if 'add' in request.POST:
            form = CompetitionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('competitions')  # Rediriger vers la même page après l'ajout
        elif 'update' in request.POST:
            competition_id = request.POST.get('id')
            competition = get_object_or_404(Competitions, pk=competition_id)
            form = CompetitionForm(request.POST, instance=competition)
            if form.is_valid():
                form.save()
                return redirect('competitions')  
        elif 'delete' in request.POST:
            competition_id = request.POST.get('id')
            competition = get_object_or_404(Competitions, pk=competition_id)
            competition.delete()
            return redirect('competitions')  
        
@user_passes_test(lambda u: u.is_superuser, login_url='/administration/login/')
def types(request):
    """ types Offre pour commande
    """
    if request.method == 'GET':
        types = Types.objects.all()
        paginator = Paginator(types,10)
        page_number = request.GET.get('page')
        page_objs = paginator.get_page(page_number)
        form = TypesForm()
        return render(request, 'types/types.html', {'page_objs': page_objs, 'form': form})
    elif request.method == 'POST':
        if 'add' in request.POST:
            form = TypesForm(request.POST)
            if form.is_valid():
                form.save()
        elif 'update' in request.POST:
            types_id = request.POST.get('id')
            types = get_object_or_404(Types, pk=types_id)
            form = TypesForm(request.POST, instance=types)
            if form.is_valid():
                form.save()
                return redirect('types')
        elif 'delete' in request.POST:
            types_id = request.POST.get('id')
            types = get_object_or_404(Types, pk=types_id)
            types.delete()
        return redirect('types')
    
@user_passes_test(lambda u: u.is_superuser, login_url='/administration/login/')
def offres(request):
    """Offre
    """
    if request.method == 'GET':
        offres = Offre.objects.all()
        paginator = Paginator(offres,10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        page_objs = Types.objects.all()
        competitions = Competitions.objects.all()
        form = OffreForm()
        return render(request, 'offres/offres.html', {'page_obj': page_obj, 'page_objs': page_objs, 'competitions': competitions, 'form': form})  
    elif request.method == 'POST':
        if 'add' in request.POST:
            form = OffreForm(request.POST)
            if form.is_valid():
                offre = form.save(commit=False)
                competition_id = request.POST.get('competition')
                if competition_id:
                    competition = get_object_or_404(Competitions, pk=competition_id)
                    offre.competition = competition
                    offre.save()
                else:
                    # Ajouter l'offre à toutes les compétitions disponibles
                    competitions = Competitions.objects.all()
                    for competition in competitions:
                        Offre.objects.create(
                            type=offre.type,
                            nombre_personnes=offre.nombre_personnes,
                            prix=offre.prix,
                            competition=competition
                        )
        elif 'update' in request.POST:
            offre_id = request.POST.get('id')
            offre = get_object_or_404(Offre, pk=offre_id)
            form = OffreForm(request.POST, instance=offre)
            if form.is_valid():
                form.save()
                return redirect('offres') 
        elif 'delete' in request.POST:
            offre_id = request.POST.get('id')
            offre = get_object_or_404(Offre, pk=offre_id)
            offre.delete()
        return redirect('offres')
    
@user_passes_test(lambda u: u.is_superuser, login_url='/administration/login/')
def commandes(request):
    """Commande
    """
    if request.method=='GET':
        commandes =Commande.objects.all()
        paginator = Paginator(commandes,10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        form = CommandeForm()
        return render(request, 'commandes/commandes.html', {'page_obj': page_obj, 'form': form})    

    if request.method == 'POST':
        if 'add' in request.POST:
            form = CommandeForm(request.POST)
            if form.is_valid():
                form.save()
        elif 'update' in request.POST:
            commande_id = request.POST.get('id')
            commande = get_object_or_404(Commande, pk=commande_id)
            form = CommandeForm(request.POST, instance=commande)
            if form.is_valid():
                form.save()
                return redirect('commandes')  
        elif 'delete' in request.POST:
            commande_id = request.POST.get('id')
            commande = get_object_or_404(Commande, pk=commande_id)
            commande.delete()
        return redirect('commandes')  
