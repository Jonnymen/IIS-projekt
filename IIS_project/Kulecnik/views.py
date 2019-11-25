from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import NewTournament_S
from .models import Tournament_S, Tournament_Players
from .forms import RegistrationForm, LoginForm, AddTournamentForm

# Create your views here.

def index(request):
    #turnaje = Tournament_S.objects.all()
    return render(request, template_name='Kulecnik/index.html', context=None)

def register(request):
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, template_name='Kulecnik/registration.html', context={'form':form})
    else:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            password = request.POST["password1"]
            user.set_password(password)
            user.save()
        return render(request, template_name='Kulecnik/index.html', context=None)

def log_out(request):
    logout(request)
    return render(request, template_name='Kulecnik/index.html', context=None)

def log_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, template_name='Kulecnik/login.html', context={'form':form})
    else:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            log_in(request)
            return render(request, template_name='Kulecnik/index.html', context=None)
        else:
            return render(request, template_name='Kulecnik/index.html', context=None)

@login_required
def add_tournament(request):

    if request.method == 'GET':
        form = AddTournamentForm()
        return render(request, template_name='Kulecnik/addtournament.html', context={'form':form})
    else:
        form = AddTournamentForm(request.POST)
        if form.is_valid():
            turnaj = form.save(commit=False)
            turnaj.host = request.user
            turnaj.save()
        return render(request, template_name='Kulecnik/index.html', context=None)

def list_tournament_s(request):
    query = Tournament_S.objects.all()
    return render(request, template_name="Kulecnik/tournament_s.html", context={'data':query})

def tournament_detail(request, row_id):
    current_tournament = Tournament_S.objects.get(pk=row_id)
    if request.method == 'GET':
        zaznamy = Tournament_Players.objects.filter(tournament=current_tournament)
        registered = Tournament_Players.objects.filter(tournament=current_tournament, player=request.user)
        if registered.count() == 0:
            return render(request, template_name='Kulecnik/tournament_detail.html', context={"tournament":current_tournament, "ucastnici":"Turnaj pro jednotlivce", "ucast":zaznamy, "registered":False})
        else:
            return render(request, template_name='Kulecnik/tournament_detail.html', context={"tournament":current_tournament, "ucastnici":"Turnaj pro jednotlivce", "ucast":zaznamy, "registered":True})
    else:
        answer = request.POST['registrovan']
        if answer == "yes":
            #Odregistrace
            Tournament_Players.objects.get(tournament=current_tournament, player=request.user).delete()
            return render(request, template_name='Kulecnik/tournament_detail.html', context={"tournament":current_tournament, "ucastnici":"Turnaj pro jednotlivce", "ucast":zaznamy, "registered":False})
        else:
            vazba = Tournament_Players(tournament=current_tournament, player=request.user)
            vazba.save()
            return render(request, template_name='Kulecnik/tournament_detail.html', context={"tournament":current_tournament, "ucastnici":"Turnaj pro jednotlivce", "ucast":zaznamy, "registered":True})




def show_profile(request):
    return render(request, template_name='Kulecnik/profile.html', context={"user":request.user})
