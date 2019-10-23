from django.urls import path, include
from Kulecnik import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    #path(r'^login/$', auth_views.login, {'template_name': 'festivaly/login.html'}, name='login'),
]