from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import NewTournament_S
from .models import Tournament_S, Tournament_T, Tournament_Players, Profile, Team
from .forms import RegistrationForm, LoginForm, AddTournamentFormS, AddTournamentFormT, EditProfileForm, EditPicture, NewTeamForm

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
            messages.success(request, "Byli jste úspěšně registrováni.")
            user = authenticate(username=form.cleaned_data['username'], password=password)
            login(request, user)
            return render(request, template_name='Kulecnik/index.html', context=None)
        else:
            messages.error(request, "Někde se stala chyba.")
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
def add_tournament_s(request):

    if request.method == 'GET':
        form = AddTournamentFormS()
        return render(request, template_name='Kulecnik/addtournament_s.html', context={'form':form})
    else:
        form = AddTournamentFormS(request.POST)
        if form.is_valid():
            turnaj = form.save(commit=False)
            turnaj.host = request.user
            turnaj.save()
        return render(request, template_name='Kulecnik/index.html', context=None)

def add_tournament_t(request):

    if request.method == 'GET':
        form = AddTournamentFormT()
        return render(request, template_name='Kulecnik/addtournament_t.html', context={'form':form})
    else:
        form = AddTournamentFormT(request.POST)
        if form.is_valid():
            turnaj = form.save(commit=False)
            turnaj.host = request.user
            turnaj.save()
        return render(request, template_name='Kulecnik/index.html', context=None)

def list_tournament_s(request):
    query = Tournament_S.objects.all()
    return render(request, template_name="Kulecnik/tournament_s.html", context={'data':query})

def tournament_detail_s(request, row_id):
    current_tournament = Tournament_S.objects.get(pk=row_id)
    zaznamy = Tournament_Players.objects.filter(tournament=current_tournament)

    if request.user.is_authenticated:
        pass
    else:
        return render(request, template_name='Kulecnik/tournament_detail.html', context={"tournament":current_tournament, "ucastnici":"Turnaj pro jednotlivce", "ucast":zaznamy, "registered":False})

    if request.method == 'GET':
        registered = Tournament_Players.objects.filter(tournament=current_tournament, player=request.user)
        if registered.count() == 0:
            return render(request, template_name='Kulecnik/tournament_detail.html', context={"tournament":current_tournament, "ucastnici":"Turnaj pro jednotlivce", "ucast":zaznamy, "registered":False})
        else:
            return render(request, template_name='Kulecnik/tournament_detail.html', context={"tournament":current_tournament, "ucastnici":"Turnaj pro jednotlivce", "ucast":zaznamy, "registered":True})
    else:
        answer = request.POST['registrovan']
        if answer == "yes":
            #Odregistrace
            Tournament_Players.objects.filter(tournament=current_tournament, player=request.user).delete()
            return render(request, template_name='Kulecnik/tournament_detail.html', context={"tournament":current_tournament, "ucastnici":"Turnaj pro jednotlivce", "ucast":zaznamy, "registered":False})
        else:
            if zaznamy.count() < current_tournament.capacity:
                registered = Tournament_Players.objects.filter(tournament=current_tournament, player=request.user)
                if registered.count() == 1:
                    return render(request, template_name='Kulecnik/message.html', context={"message":"Na tento turnaj už jsi zaregistrovaný", "back":"/tournament_s/" + str(row_id) + "/"})
                vazba = Tournament_Players(tournament=current_tournament, player=request.user)
                vazba.save()
                return render(request, template_name='Kulecnik/tournament_detail.html', context={"tournament":current_tournament, "ucastnici":"Turnaj pro jednotlivce", "ucast":zaznamy, "registered":True})
            else:
                return render(request, template_name='Kulecnik/message.html', context={"message":"Kapacita účastníků turnaje je zaplněná", "back":"/tournament_s/" + str(row_id) + "/"})

def list_tournament_t(request):
    query = Tournament_T.objects.all()
    return render(request, template_name="Kulecnik/tournament_t.html", context={'data':query})

def team_detail(request, team_id):
    team = Team.objects.get(pk=team_id)
    if team is None:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Hledaný tým neexistuje!"})
    else:
        return render(request, template_name='Kulecnik/team_detail.html', context={'team':team})

def add_player_to_team(request, team_id):
    team = Team.objects.get(id=team_id)
    if team is None:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Hledaný tým neexistuje!"})
    if team.captain is not request.user:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Nejsi autorizovaný přidat hráče do týmu, ve kterém nejsi kapitán!"})
    if request.method == 'GET':
        return render(request, template_name='Kulecnik/addplayertoteam.html', context={'team_id':team_id})
    else:
        team = Team.objects.get(id=request.POST['team'])
        if team is None:
            return render(request, template_name='Kulecnik/message.html', context={"message":"Tým neexistuje!"})
        player_name = request.POST['player']
        spec_user = User.objects.get(username=player_name)
        if spec_user is None:
            return render(request, template_name='Kulecnik/addplayertoteam.html', context={'team_id':team_id, 'failure':"Zvoleý hráč neexistuje!"})
        else:
            if team.player is not None:
                return render(request, template_name='Kulecnik/message.html', context={"message":"Tým je plný!"})
            else:
                team.player = spec_user
                team.save()
                return redirect("/team/" + team_id + "/")


def show_profile(request):
    return render(request, template_name='users/profile.html', context={"user":request.user})

def edit_profile(request):
    if request.method == 'GET':
        form = EditProfileForm(instance=request.user)
        picture = EditPicture(instance=request.user.profile)
        return render(request, template_name='users/edit_profile.html', context={"form":form, "picture":picture})
    else:
        form = EditProfileForm(request.POST, instance=request.user)
        picture = EditPicture(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and picture.is_valid():
            form.save()
            picture.save()
            return redirect('/profile/')

def player_detail(request, row_id):
    current_user = User.objects.get(pk=row_id)
    return render(request, template_name='users/profile_view.html', context={"user":current_user})

def edit_password(request):
    if request.method == 'GET':
        form = PasswordChangeForm(user=request.user)
        return render(request, template_name='users/edit_password.html', context={"form":form})
    else:
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) #to stay logged in after password change
            return redirect('/profile/')
        else:
            return render(request, template_name='users/edit_password.html', context={"form":form, "string":"error"})

def new_team(request):
    if request.method == 'GET':
        form = NewTeamForm()
        return render(request, template_name='Kulecnik/new_team.html', context={'form':form})
    else:
        form = NewTeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            check_teams = Team.objects.filter(name=team.name)
            if check_teams.count() > 0:
                return render(request, template_name='Kulecnik/new_team.html', context={'form':form, 'failure':"Tým s tímto názvem již existuje, vyberte prosím jiný název"})
            team.captain = request.user
            team.save()
            return render(request, template_name='Kulecnik/new_team.html', context={'form':form, 'success':"Tým byl vytvořen!"})
        else:
            return render(request, template_name='Kulecnik/new_team.html', context={'form':form, 'failure':"Tým nebylo možné vytvořit (název je moc dlouhý nebo obsahuje nepovolené znaky!"})

def my_teams(request):
    teams_as_captain = Team.objects.filter(captain=request.user)
    teams_as_player = Team.objects.filter(player=request.user)
    return render(request, template_name="Kulecnik/my_teams.html", context={'teams_c':teams_as_captain, 'teams_p':teams_as_player})
