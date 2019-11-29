import random
import math
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import NewTournament_S
from .models import Tournament_S, Tournament_T, Tournament_Players, Tournament_Teams, Profile, Team, Game_T, Game_S
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
            user_profile = Profile(user=user)
            user_profile.save()
            messages.success(request, "Byli jste úspěšně registrováni.")
            user = authenticate(username=form.cleaned_data['username'], password=password)
            login(request, user)
            return render(request, template_name='Kulecnik/index.html', context={'result':"success"})
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
    pocet = Tournament_Players.objects.filter(tournament=current_tournament, registered=True).count()
    zapasy = Game_S.objects.filter(tournament=current_tournament)
    
    if request.user.is_authenticated:
        pass
    else:
        return render(request, template_name='Kulecnik/tournament_detail.html', context={"tournament":current_tournament, "ucastnici":"Turnaj pro jednotlivce", "ucast":zaznamy, "registered":False, "pocet":pocet, "zapasy":zapasy})

    if request.method == 'GET':
        registered = Tournament_Players.objects.filter(tournament=current_tournament, player=request.user)
        if registered.count() == 0:
            return render(request, template_name='Kulecnik/tournament_detail.html', context={"tournament":current_tournament, "ucastnici":"Turnaj pro jednotlivce", "ucast":zaznamy, "registered":False, "pocet":pocet, "zapasy":zapasy})
        else:
            return render(request, template_name='Kulecnik/tournament_detail.html', context={"tournament":current_tournament, "ucastnici":"Turnaj pro jednotlivce", "ucast":zaznamy, "registered":True, "pocet":pocet, "zapasy":zapasy})
    else:
        answer = request.POST['registrovan']
        if answer == "yes":
            #Odregistrace
            Tournament_Players.objects.filter(tournament=current_tournament, player=request.user).delete()
            return render(request, template_name='Kulecnik/tournament_detail.html', context={"tournament":current_tournament, "ucastnici":"Turnaj pro jednotlivce", "ucast":zaznamy, "registered":False, "pocet":pocet, "zapasy":zapasy})
        else:
            registered = Tournament_Players.objects.filter(tournament=current_tournament, player=request.user)
            if registered.count() == 1:
                return render(request, template_name='Kulecnik/message.html', context={"message":"Na tento turnaj už jsi zaregistrovaný", "back":"/tournament_s/" + str(row_id) + "/"})
            vazba = Tournament_Players(tournament=current_tournament, player=request.user)
            vazba.save()
            return render(request, template_name='Kulecnik/tournament_detail.html', context={"tournament":current_tournament, "ucastnici":"Turnaj pro jednotlivce", "ucast":zaznamy, "registered":True, "pocet":pocet, "zapasy":zapasy})

def list_tournament_t(request):
    query = Tournament_T.objects.all()
    return render(request, template_name="Kulecnik/tournament_t.html", context={'data':query})

def tournament_detail_t(request, row_id):
    current_tournament = Tournament_T.objects.get(pk=row_id)
    zaznamy = Tournament_Teams.objects.filter(tournament=current_tournament)
    pocet = Tournament_Teams.objects.filter(tournament=current_tournament, registered=True).count()
    is_past = (datetime.today() > current_tournament.reg_deadline)
    if request.user.is_authenticated:
        pass
    else:
        return render(request, template_name='Kulecnik/tournament_detail_t.html', context={"tournament":current_tournament, "ucast":zaznamy, "registered":False, "pocet": pocet})

    if request.method == 'GET':
        player_teams = Team.objects.filter(captain=request.user)
        registered = Tournament_Teams.objects.filter(tournament=current_tournament, team__captain=request.user)

        if registered.count() == 0:
            return render(request, template_name='Kulecnik/tournament_detail_t.html', context={"tournament":current_tournament, "ucast":zaznamy, "registered":False, "player_teams":player_teams, "pocet": pocet})
        else:
            return render(request, template_name='Kulecnik/tournament_detail_t.html', context={"tournament":current_tournament, "ucast":zaznamy, "registered":True, "player_teams":player_teams, "pocet": pocet})

    else:
        player_teams = Team.objects.filter(captain=request.user)
        answer = request.POST['registrovan']
        if answer == "yes":
            #Odregistrace
            Tournament_Teams.objects.filter(tournament=current_tournament, team__captain=request.user).delete()
            return render(request, template_name='Kulecnik/tournament_detail_t.html', context={"tournament":current_tournament, "ucast":zaznamy, "registered":False, "player_teams":player_teams, "pocet": pocet})
        else:
            try:
                team = request.POST['team']
                team = Team.objects.get(id=team)
                Tournament_Teams(tournament=current_tournament, team=team).save()
                return render(request, template_name='Kulecnik/tournament_detail_t.html', context={"tournament":current_tournament, "ucast":zaznamy, "registered":True, "player_teams":player_teams, "pocet": pocet})
            except:
                return render(request, template_name='Kulecnik/tournament_detail_t.html', context={"tournament":current_tournament, "ucast":zaznamy, "registered":False, "player_teams":player_teams, "pocet": pocet})

def team_detail(request, team_id):
    team = Team.objects.get(pk=team_id)
    #player = team.player
    if team is None:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Hledaný tým neexistuje!"})
    else:
        return render(request, template_name='Kulecnik/team_detail.html', context={'team':team})

def add_player_to_team(request, team_id):
    team = Team.objects.get(id=team_id)
    if team is None:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Hledaný tým neexistuje!"})
    if team.captain.pk is not request.user.pk:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Nejsi autorizovaný přidat hráče do týmu, ve kterém nejsi kapitán!", "back":"/team/" + str(team_id) + "/"})
    if request.method == 'GET':
        if team.player is not None:
            return render(request, template_name='Kulecnik/message.html', context={"message":"Tým je plný!", "back":"/team/" + str(team_id) + "/"})
        else:
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
                return redirect("/team/" + str(team_id) + "/")

def remove_player_from_team(request, team_id):
    team = Team.objects.get(id=team_id)
    if team is None:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Hledaný tým neexistuje!"})
    if team.captain.pk is not request.user.pk:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Nejsi autorizovaný odebrat hráče z týmu, ve kterém nejsi kapitán!", "back":"/team/" + str(team_id) + "/"})
    team.player = None
    team.save()
    return redirect("/team/" + str(team_id) + "/")

def delete_team(request, team_id):
    team = Team.objects.get(id=team_id)
    if team is None:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Hledaný tým neexistuje!"})
    if team.captain.pk is not request.user.pk:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Nejsi autorizovaný smazat tým, ve kterém nejsi kapitán!", "back":"/team/" + str(team_id) + "/"})
    if request.method == 'GET':
        return render(request, template_name='Kulecnik/confirmation.html', context={"message":"Určitě si přeješ smazat tým " + team.name + "?", "cancel_href":"/team/" + str(team_id) + "/"})
    else:
        # request POST if user chooses 'yes' in confirmation
        team.delete()
        return redirect("/my_teams/")

def leave_team(request, team_id):
    team = Team.objects.get(id=team_id)
    if team is None:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Hledaný tým neexistuje!"})
    if team.player.pk is not request.user.pk:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Nejsi autorizovaný vystoupit z týmu, ve kterém nejsi!", "back":"/team/" + str(team_id) + "/"})
    team.player = None
    team.save()
    return redirect("/my_teams/")

def show_profile(request):
    my_tournaments_s = Tournament_S.objects.filter(host=request.user)
    my_tournaments_t = Tournament_T.objects.filter(host=request.user)
    my_tournaments_s_link = Tournament_Players.objects.filter(tournament__host=request.user)
    my_tournaments_t_link = Tournament_Teams.objects.filter(tournament__host=request.user)
    return render(request, template_name='users/profile.html', context={"user":request.user, "my_tournaments_s":my_tournaments_s, "my_tournaments_t":my_tournaments_t, "my_tournaments_s_link":my_tournaments_s_link, "my_tournaments_t_link":my_tournaments_t_link})

def confirm_team(request, tournament_id, team_id):
    tournament = Tournament_T.objects.get(id=tournament_id)
    team = Team.objects.get(id=team_id)
    link = Tournament_Teams.objects.get(team=team, tournament=tournament)
    link.registered = True
    link.save()
    return redirect("/tournament_t/" + str(tournament_id) + "/")

def deny_team(request, tournament_id, team_id):
    tournament = Tournament_T.objects.get(id=tournament_id)
    team = Team.objects.get(id=team_id)
    link = Tournament_Teams.objects.get(team=team, tournament=tournament)
    link.delete()
    return redirect("/tournament_t/" + str(tournament_id) + "/")

def confirm_player(request, tournament_id, player_id):
    tournament = Tournament_S.objects.get(id=tournament_id)
    pocet = Tournament_Players.objects.filter(tournament=tournament, registered=True).count()
    if request.user.id is not tournament.host.id:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Nemůžeš spravovat žádosti, nejsi pořadatelem turnaje!", "back":"/tournament_s/" + str(tournament_id) + "/"})
    if pocet == tournament.capacity:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Turnaj je zaplněn!", "back":"/tournament_s/" + str(tournament_id) + "/"})
    player = User.objects.get(id=player_id)
    link = Tournament_Players.objects.get(player=player, tournament=tournament)
    link.registered = True
    link.save()
    return redirect("/tournament_s/" + str(tournament_id) + "/")

def deny_player(request, tournament_id, player_id):
    tournament = Tournament_S.objects.get(id=tournament_id)
    if request.user.id is not tournament.host.id:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Nemůžeš spravovat žádosti, nejsi pořadatelem turnaje!", "back":"/tournament_s/" + str(tournament_id) + "/"})
    player = User.objects.get(id=player_id)
    link = Tournament_Players.objects.get(player=player, tournament=tournament)
    link.delete()
    return redirect("/tournament_s/" + str(tournament_id) + "/")

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
            return redirect("/team/" + str(team.id) + "/")
        else:
            return render(request, template_name='Kulecnik/new_team.html', context={'form':form, 'failure':"Tým nebylo možné vytvořit (název je moc dlouhý nebo obsahuje nepovolené znaky!"})

def my_teams(request):
    teams_as_captain = Team.objects.filter(captain=request.user)
    teams_as_player = Team.objects.filter(player=request.user)
    return render(request, template_name="Kulecnik/my_teams.html", context={'teams_c':teams_as_captain, 'teams_p':teams_as_player})

def game_generator_t(request, tournament_id):

    current_tournament = Tournament_T.objects.get(id=tournament_id)
    games = Game_T.objects.filter(tournament=current_tournament)

    if games.count() > 0:
        return redirect("/tournament_t/" + str(tournament_id) + "/")

    zaznamy = Tournament_Teams.objects.filter(tournament=current_tournament)
    stages = math.log2(current_tournament.capacity)
    all_teams = list(zaznamy)
    random.shuffle(all_teams)
    next_stage = None
    game_list = []
    tmp_list = []
    stage = 1

    while len(all_teams) > 0:
        team_1 = all_teams.pop(0)
        try:
            team_2 = all_teams.pop(0)
        except:
            team_2 = None
        game = Game_T(team_1=team_1.team, team_2=team_2.team, tournament=current_tournament, stage=stage)
        game.save()
        game_list.append(game)

    while stages > 1:
        while len(game_list) > 1:
            next_stage = Game_T(tournament=current_tournament, stage=stage + 1)
            next_stage.save()
            tmp_list.append(next_stage)
            game_1 = game_list.pop(0)
            game_1.next_game_id = next_stage
            game_1.save()
            game_2 = game_list.pop(0)
            game_2.next_game_id = next_stage
            game_2.save()

        game_list = tmp_list[:]
        tmp_list.clear()
        stages -= 1
        stage += 1
    return redirect("/tournament_t/" + str(tournament_id) + "/")

def game_bracket(request, tournament_id):
    tournament = Tournament_T.objects.get(id=tournament_id)
    stages_no = math.log2(tournament.capacity)
    stages = []
    i = 1
    while i <= stages_no:
        stages.append(i)
        i += 1
    games = Game_T.objects.filter(tournament=tournament)
    return render(request, template_name='Kulecnik/games_bracket.html', context={'stages':stages, 'tournament':tournament, 'games':games})
