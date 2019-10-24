from django.urls import path, include
from Kulecnik import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), {'template_name':'Kulecnik/login.html'}),
    path('logout/', views.log_out, name='logout'),
    path('add_tournament/', views.add_tournament, name='date')
    #path('addtournament_s/', views.addTournament_S, name="addTournament_S")
    #path(r'^login/$', auth_views.login, {'template_name': 'festivaly/login.html'}, name='login'),
]