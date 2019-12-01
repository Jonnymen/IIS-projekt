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
from django.utils import timezone
from .forms import NewTournament_S
from .models import (Tournament_S, Tournament_T, Tournament_Players, Tournament_Teams,
                     Profile, Team, Game_T, Game_S, Tournament_S_referees, Tournament_T_referees)
from .forms import RegistrationForm, LoginForm, AddTournamentFormS, AddTournamentFormT, EditProfileForm, EditPicture, NewTeamForm, EditLogo

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
    query = Tournament_S.objects.all().order_by('start_date', 'reg_deadline')
    return render(request, template_name="Kulecnik/tournament_s.html", context={'data':query})

def tournament_detail_s(request, row_id):
    current_tournament = Tournament_S.objects.get(pk=row_id)
    zaznamy = Tournament_Players.objects.filter(tournament=current_tournament)
    pocet = Tournament_Players.objects.filter(tournament=current_tournament, registered=True).count()
    zapasy = Game_S.objects.filter(tournament=current_tournament)
    rozhodci = Tournament_S_referees.objects.filter(tournament=current_tournament)
    if request.user.is_authenticated:
        if_referee = Tournament_S_referees.objects.filter(tournament=current_tournament, referee=request.user).count()
    else:
        if_referee = 0
    today = timezone.now()
    is_past = (today > current_tournament.reg_deadline)

    if request.user.is_authenticated:
        pass
    else:
        return render(request, template_name='Kulecnik/tournament_detail.html', context={"tournament":current_tournament, "ucastnici":"Turnaj pro jednotlivce", "ucast":zaznamy, "registered":False, "pocet":pocet, "zapasy":zapasy, "rozhodci":rozhodci, "if_referee":if_referee, "is_past":is_past})

    if request.method == 'GET':
        registered = Tournament_Players.objects.filter(tournament=current_tournament, player=request.user)
        if registered.count() == 0:
            return render(request, template_name='Kulecnik/tournament_detail.html', context={"tournament":current_tournament, "ucastnici":"Turnaj pro jednotlivce", "ucast":zaznamy, "registered":False, "pocet":pocet, "zapasy":zapasy, "rozhodci":rozhodci, "if_referee":if_referee, "is_past":is_past})
        else:
            return render(request, template_name='Kulecnik/tournament_detail.html', context={"tournament":current_tournament, "ucastnici":"Turnaj pro jednotlivce", "ucast":zaznamy, "registered":True, "pocet":pocet, "zapasy":zapasy, "rozhodci":rozhodci, "if_referee":if_referee, "is_past":is_past})
    else:
        answer = request.POST['registrovan']
        if answer == "yes":
            #Odregistrace
            Tournament_Players.objects.filter(tournament=current_tournament, player=request.user).delete()
            return redirect("/tournament_s/" + str(row_id) + "/")
        else:
            referee = Tournament_S_referees.objects.filter(tournament=current_tournament, referee=request.user)
            if referee.count() == 1:
                return render(request, template_name='Kulecnik/message.html', context={"message":"Na tento turnaj už jsi zaregistrovaný jako rozhodčí", "back":"/tournament_s/" + str(row_id) + "/"})
            registered = Tournament_Players.objects.filter(tournament=current_tournament, player=request.user)
            if registered.count() == 1:
                return render(request, template_name='Kulecnik/message.html', context={"message":"Na tento turnaj už jsi zaregistrovaný", "back":"/tournament_s/" + str(row_id) + "/"})
            vazba = Tournament_Players(tournament=current_tournament, player=request.user)
            vazba.save()
            return render(request, template_name='Kulecnik/tournament_detail.html', context={"tournament":current_tournament, "ucastnici":"Turnaj pro jednotlivce", "ucast":zaznamy, "registered":True, "pocet":pocet, "zapasy":zapasy, "rozhodci":rozhodci, "if_referee":if_referee, "is_past":is_past})

def reg_referee(request, row_id, ref_id):
    current_tournament = Tournament_S.objects.get(id=row_id)
    player_check = Tournament_Players.objects.filter(tournament=current_tournament, player=request.user).count()
    if player_check != 0:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Na tento turnaj už jsi zaregistrovaný jako hráč", "back":"/tournament_s/" + str(row_id) + "/"})
    if ref_id == request.user.id or request.user.is_superuser:
        Tournament_S_referees(tournament=current_tournament, referee=request.user).save()
        return redirect("/tournament_s/" + str(row_id) + "/")
    else:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Nemůžeš přihlásit jiného uživatele jako rozhodčího", "back":"/tournament_s/" + str(row_id) + "/"})

def unreg_referee(request, row_id, ref_id):
    current_tournament = Tournament_S.objects.get(id=row_id)
    referee = User.objects.get(id=ref_id)
    vazba = Tournament_S_referees.objects.filter(tournament=current_tournament, referee=referee)
    vazba.delete()
    return redirect("/tournament_s/" + str(row_id) + "/")

def confirm_referee(request, row_id, ref_id):
    current_tournament = Tournament_S.objects.get(id=row_id)
    referee = User.objects.get(id=ref_id)
    ref = Tournament_S_referees.objects.get(tournament=current_tournament, referee=referee)
    ref.registered = True
    ref.save()
    return redirect("/tournament_s/" + str(row_id) + "/")

def reg_referee_t(request, row_id, ref_id):
    current_tournament = Tournament_T.objects.get(id=row_id)
    teams = Tournament_Teams.objects.filter(tournament=current_tournament)
    for row in teams:
        if row.team.captain is request.user or row.team.player is request.user:
            return render(request, template_name='Kulecnik/message.html', context={"message":"Na tento turnaj už jsi zaregistrovaný jako hráč", "back":"/tournament_t/" + str(row_id) + "/"})
    if ref_id == request.user.id or request.user.is_superuser:
        Tournament_T_referees(tournament=current_tournament, referee=request.user).save()
        return redirect("/tournament_t/" + str(row_id) + "/")
    else:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Nemůžeš přihlásit jiného uživatele jako rozhodčího", "back":"/tournament_t/" + str(row_id) + "/"})

def unreg_referee_t(request, row_id, ref_id):
    current_tournament = Tournament_T.objects.get(id=row_id)
    referee = User.objects.get(id=ref_id)
    vazba = Tournament_T_referees.objects.filter(tournament=current_tournament, referee=referee)
    vazba.delete()
    return redirect("/tournament_t/" + str(row_id) + "/")

def confirm_referee_t(request, row_id, ref_id):
    current_tournament = Tournament_T.objects.get(id=row_id)
    referee = User.objects.get(id=ref_id)
    ref = Tournament_T_referees.objects.get(tournament=current_tournament, referee=referee)
    ref.registered = True
    ref.save()
    return redirect("/tournament_t/" + str(row_id) + "/")

def list_tournament_t(request):
    query = Tournament_T.objects.all().order_by('start_date', 'reg_deadline')
    return render(request, template_name="Kulecnik/tournament_t.html", context={'data':query})

def tournament_detail_t(request, row_id):
    current_tournament = Tournament_T.objects.get(pk=row_id)
    zaznamy = Tournament_Teams.objects.filter(tournament=current_tournament)
    pocet = Tournament_Teams.objects.filter(tournament=current_tournament, registered=True).count()
    rozhodci = Tournament_T_referees.objects.filter(tournament=current_tournament)
    if request.user.is_authenticated:
        if_referee = Tournament_T_referees.objects.filter(tournament=current_tournament, referee=request.user).count()
    else:
        if_referee = 0
    today = timezone.now()
    is_past = (today > current_tournament.reg_deadline)
    if request.user.is_authenticated:
        pass
    else:
        return render(request, template_name='Kulecnik/tournament_detail_t.html', context={"tournament":current_tournament, "ucast":zaznamy, "registered":False, "pocet": pocet, "rozhodci":rozhodci, "if_referee":if_referee, "is_past":is_past})

    if request.method == 'GET':
        player_teams = Team.objects.filter(captain=request.user)
        registered = Tournament_Teams.objects.filter(tournament=current_tournament, team__captain=request.user)

        if registered.count() == 0:
            return render(request, template_name='Kulecnik/tournament_detail_t.html', context={"tournament":current_tournament, "ucast":zaznamy, "registered":False, "player_teams":player_teams, "pocet": pocet, "rozhodci":rozhodci, "if_referee":if_referee, "is_past":is_past})
        else:
            return render(request, template_name='Kulecnik/tournament_detail_t.html', context={"tournament":current_tournament, "ucast":zaznamy, "registered":True, "player_teams":player_teams, "pocet": pocet, "rozhodci":rozhodci, "if_referee":if_referee, "is_past":is_past})

    else:
        player_teams = Team.objects.filter(captain=request.user)
        answer = request.POST['registrovan']
        if answer == "yes":
            #Odregistrace
            Tournament_Teams.objects.filter(tournament=current_tournament, team__captain=request.user).delete()
            return redirect("/tournament_t/" + str(row_id) + "/")
        else:
            try:
                team = request.POST['team']
                team = Team.objects.get(id=team)
                Tournament_Teams(tournament=current_tournament, team=team).save()
                return render(request, template_name='Kulecnik/tournament_detail_t.html', context={"tournament":current_tournament, "ucast":zaznamy, "registered":True, "player_teams":player_teams, "pocet": pocet, "rozhodci":rozhodci, "if_referee":if_referee, "is_past":is_past})
            except:
                return render(request, template_name='Kulecnik/tournament_detail_t.html', context={"tournament":current_tournament, "ucast":zaznamy, "registered":False, "player_teams":player_teams, "pocet": pocet, "rozhodci":rozhodci, "if_referee":if_referee, "is_past":is_past})

def team_detail(request, team_id):
    team = Team.objects.get(pk=team_id)
    if request.method == 'GET':
        logo = EditLogo(instance=team)
        if team is None:
            return render(request, template_name='Kulecnik/message.html', context={"message":"Hledaný tým neexistuje!"})
        else:
            return render(request, template_name='Kulecnik/team_detail.html', context={'team':team, "logo":logo})
    else:
        logo = EditLogo(request.POST, request.FILES, instance=team)
        if logo.is_valid():
            logo.save()
            return redirect('/team/' + str(team_id) + '/')

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

@login_required
def show_profile(request):
    poradane = Tournament_S.objects.filter(host=request.user)
    ucastnene = Tournament_Players.objects.filter(player=request.user)
    tymy_poradane = Tournament_T.objects.filter(host=request.user)
    won_tournaments_s = Tournament_S.objects.filter(winner=request.user).count()
    all_tournaments_s = Tournament_S.objects.all().count()
    won_games_s = Game_S.objects.filter(winner=request.user).count()
    all_games_s = Game_S.objects.filter(player_1=request.user).count() + Game_S.objects.filter(player_2=request.user).count()
    if all_tournaments_s == 0:
        tournament_s_winrate = 0
    else:
        tournament_s_winrate = won_tournaments_s / all_tournaments_s
    if all_games_s == 0:
        game_s_winrate = 0
    else:
        game_s_winrate = won_games_s / all_games_s
    return render(request, template_name='users/profile.html', context={"poradane":poradane, "ucastnene":ucastnene, "tymy_poradane":tymy_poradane, "won_tournaments":won_tournaments_s, "won_games":won_games_s, "tournament_winrate":tournament_s_winrate, "game_winrate":game_s_winrate})

def confirm_team(request, tournament_id, team_id):
    tournament = Tournament_T.objects.get(id=tournament_id)
    pocet = Tournament_Teams.objects.filter(tournament=tournament, registered=True).count()
    if request.user.id is not tournament.host.id and request.user.is_superuser is False:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Nemůžeš spravovat žádosti, nejsi pořadatelem turnaje!", "back":"/tournament_t/" + str(tournament_id) + "/"})
    if pocet >= tournament.capacity:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Turnaj je zaplněn!", "back":"/tournament_t/" + str(tournament_id) + "/"})
    team = Team.objects.get(id=team_id)
    link = Tournament_Teams.objects.get(team=team, tournament=tournament)
    link.registered = True
    link.save()
    return redirect("/tournament_t/" + str(tournament_id) + "/")

def deny_team(request, tournament_id, team_id):
    tournament = Tournament_T.objects.get(id=tournament_id)
    if request.user.id is not tournament.host.id and request.user.is_superuser is False:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Nemůžeš spravovat žádosti, nejsi pořadatelem turnaje!", "back":"/tournament_t/" + str(tournament_id) + "/"})
    team = Team.objects.get(id=team_id)
    link = Tournament_Teams.objects.get(team=team, tournament=tournament)
    link.delete()
    return redirect("/tournament_t/" + str(tournament_id) + "/")

def confirm_player(request, tournament_id, player_id):
    tournament = Tournament_S.objects.get(id=tournament_id)
    pocet = Tournament_Players.objects.filter(tournament=tournament, registered=True).count()
    if request.user.id is not tournament.host.id and request.user.is_superuser is False:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Nemůžeš spravovat žádosti, nejsi pořadatelem turnaje!", "back":"/tournament_s/" + str(tournament_id) + "/"})
    if pocet >= tournament.capacity:
        return render(request, template_name='Kulecnik/message.html', context={"message":"Turnaj je zaplněn!", "back":"/tournament_s/" + str(tournament_id) + "/"})
    player = User.objects.get(id=player_id)
    link = Tournament_Players.objects.get(player=player, tournament=tournament)
    link.registered = True
    link.save()
    return redirect("/tournament_s/" + str(tournament_id) + "/")

def deny_player(request, tournament_id, player_id):
    tournament = Tournament_S.objects.get(id=tournament_id)
    if request.user.id is not tournament.host.id and request.user.is_superuser is False:
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
        games.delete()

    zaznamy = Tournament_Teams.objects.filter(tournament=current_tournament)
    stages = math.log2(current_tournament.capacity)
    capacity = current_tournament.capacity / 2
    all_teams = list(zaznamy)
    random.shuffle(all_teams)
    next_stage = None
    game_list = []
    tmp_list = []
    stage = 1

    while capacity > 0:
        try:
            team_1 = all_teams.pop(0)
            team_1 = team_1.team
        except:
            team_1 = None

        try:
            team_2 = all_teams.pop(0)
            team_2 = team_2.team
        except:
            team_2 = None

        if team_2 is None:
            game = Game_T(team_1=team_1, team_2=team_2, tournament=current_tournament, stage=stage, winner=team_1)
        else:
            game = Game_T(team_1=team_1, team_2=team_2, tournament=current_tournament, stage=stage)
        game.save()
        game_list.append(game)
        capacity -= 1

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
    return redirect("/bracket/" + str(tournament_id) + "/")

def game_generator_s(request, tournament_id):
    current_tournament = Tournament_S.objects.get(id=tournament_id)
    games = Game_S.objects.filter(tournament=current_tournament)

    if games.count() > 0:
        games.delete()

    zaznamy = Tournament_Players.objects.filter(tournament=current_tournament)
    stages = math.log2(current_tournament.capacity)
    capacity = current_tournament.capacity / 2
    all_teams = list(zaznamy)
    random.shuffle(all_teams)
    next_stage = None
    game_list = []
    tmp_list = []
    stage = 1

    while capacity > 0:
        try:
            team_1 = all_teams.pop(0)
            team_1 = team_1.player
        except:
            team_1 = None

        try:
            team_2 = all_teams.pop(0)
            team_2 = team_2.player
        except:
            team_2 = None

        if team_2 is None:
            game = Game_S(player_1=team_1, player_2=team_2, tournament=current_tournament, stage=stage, winner=team_1)
        else:
            game = Game_S(player_1=team_1, player_2=team_2, tournament=current_tournament, stage=stage)
        game.save()
        game_list.append(game)
        capacity -= 1

    while stages > 1:
        while len(game_list) > 1:
            next_stage = Game_S(tournament=current_tournament, stage=stage + 1)
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
    return redirect("/bracket_s/" + str(tournament_id) + "/")

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

def game_bracket_s(request, tournament_id):
    tournament = Tournament_S.objects.get(id=tournament_id)
    stages_no = math.log2(tournament.capacity)
    stages = []
    i = 1
    while i <= stages_no:
        stages.append(i)
        i += 1
    games = Game_S.objects.filter(tournament=tournament)
    return render(request, template_name='Kulecnik/games_bracket_s.html', context={'stages':stages, 'tournament':tournament, 'games':games})

def list_games_t(request, tournament_id):
    tournament = Tournament_T.objects.get(id=tournament_id)
    try:
        link = Tournament_T_referees.objects.get(tournament=tournament, referee=request.user)
    except:
        link = None

    if link is None:
        is_referee = False
    else:
        is_referee = True
    stages_no = math.log2(tournament.capacity)
    stages = []
    i = 1
    while i <= stages_no:
        stages.append(i)
        i += 1
    games = Game_T.objects.filter(tournament=tournament)
    return render(request, template_name="Kulecnik/games_t.html", context={'games':games, 'stages':stages, 'is_referee':is_referee})

def list_games_s(request, tournament_id):
    tournament = Tournament_S.objects.get(id=tournament_id)
    stages_no = math.log2(tournament.capacity)
    stages = []
    i = 1
    while i <= stages_no:
        stages.append(i)
        i += 1
    games = Game_S.objects.filter(tournament=tournament)
    return render(request, template_name="Kulecnik/games_s.html", context={'games':games, 'stages':stages})

def select_winner_t(request, game_id, team_id):
    game = Game_T.objects.get(id=game_id)
    team = Team.objects.get(id=team_id)
    next_game = game.next_game
    game.winner = team
    if next_game is not None:
        second_game = Game_T.objects.exclude(id=game_id).get(next_game=game.next_game)
        if game.id < second_game.id:
            next_game.team_1 = game.winner
        else:
            next_game.team_2 = game.winner
        next_game.save()
    else:
        tournament = game.tournament
        tournament.winner = game.winner
        tournament.save()
    game.save()
    return redirect("/games_t/" + str(game.tournament.id) + "/")

def select_winner_s(request, game_id, player_id):
    game = Game_S.objects.get(id=game_id)
    player = User.objects.get(id=player_id)
    next_game = game.next_game
    game.winner = player
    if next_game is not None:
        second_game = Game_T.objects.exclude(id=game_id).get(next_game=game.next_game)
        if game.id < second_game.id:
            next_game.player_1 = game.winner
        else:
            next_game.player_2 = game.winner
        next_game.save()
    else:
        tournament = game.tournament
        tournament.winner = game.winner
        tournament.save()
    game.save()
    return redirect("/games_s/" + str(game.tournament.id) + "/")
