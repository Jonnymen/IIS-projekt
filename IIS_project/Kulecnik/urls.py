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
    path('add_tournament/', views.add_tournament, name='date'),
    path('list_tournament_s/', views.list_tournament_s, name='list_tournament_s'),
    path('tournament_s/<int:row_id>/', views.tournament_detail_s, name='tournament_detail'),
    path('list_tournament_t/', views.list_tournament_t, name='list_tournament_t'),
    #path('tournament_t/<int:row_id>/', views.tournament_detail_t, name='tournament_detail'),
    path('team/<int:team_id>/', views.team_detail, name='team_detail'),
    path('profile/', views.show_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/edit/password/', views.edit_password, name='edit_password'),
    path('profile_page/<int:row_id>/', views.player_detail, name='player_detail'),
    path('new_team/', views.new_team, name='new_team'),
    path('my_teams/', views.my_teams, name='my_teams')
    #path('addtournament_s/', views.addTournament_S, name="addTournament_S")
    #path(r'^login/$', auth_views.login, {'template_name': 'festivaly/login.html'}, name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
