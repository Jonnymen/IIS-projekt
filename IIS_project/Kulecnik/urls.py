from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), {'template_name':'Kulecnik/login.html'}),
    path('logout/', views.log_out, name='logout'),
    path('add_tournament_s/', views.add_tournament_s, name='date'),
    path('add_tournament_t/', views.add_tournament_t, name='date'),
    path('list_tournament_s/', views.list_tournament_s, name='list_tournament_s'),
    path('tournament_s/<int:row_id>/', views.tournament_detail_s, name='tournament_detail'),
    path('list_tournament_t/', views.list_tournament_t, name='list_tournament_t'),
    path('tournament_t/<int:row_id>/', views.tournament_detail_t, name='tournament_detail'),
    path('team/<int:team_id>/', views.team_detail, name='team_detail'),
    path('team/<int:team_id>/addplayer/', views.add_player_to_team, name='views.add_player_to_team'),
    path('team/<int:team_id>/removeplayer/', views.remove_player_from_team, name='remove_player_from_team'),
    path('team/<int:team_id>/delete/', views.delete_team, name='delete_team'),
    path('team/<int:team_id>/leave/', views.leave_team, name='leave_team'),
    path('profile/', views.show_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/edit/password/', views.edit_password, name='edit_password'),
    path('profile_page/<int:row_id>/', views.player_detail, name='player_detail'),
    path('new_team/', views.new_team, name='new_team'),
    path('my_teams/', views.my_teams, name='my_teams'),
    path('tournament_s/<int:tournament_id>/confirm_s/<int:player_id>/', views.confirm_player, name='confirm_player'),
    path('tournament_s/<int:tournament_id>/deny_s/<int:player_id>/', views.deny_player, name='confirm_player'),
    path('<int:tournament_id>/confirm_t/<int:team_id>/', views.confirm_team, name='confirm_team'),
    path('<int:tournament_id>/deny_t/<int:team_id>/', views.deny_team, name='deny_team'),
    path('generate/<int:tournament_id>/', views.game_generator_t, name='game_generator_t'),
    path('bracket/', views.game_bracket, name='game_bracket')
    #path('addtournament_s/', views.addTournament_S, name="addTournament_S")
    #path(r'^login/$', auth_views.login, {'template_name': 'festivaly/login.html'}, name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
