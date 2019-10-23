from django.shortcuts import render
from django.http import HttpResponse
from .forms import NewTournament_S
from .models import Tournament_S
from .forms import RegistrationForm

# Create your views here.

def index(request):
    turnaje = Tournament_S.objects.all()
    return render(request, template_name='Kulecnik/index.html', context={'tur': turnaje})

def register(request):
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, template_name='Kulecnik/registration.html', context={'form':form})
    else:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
        return render(request, template_name='Kulecnik/index.html', context=None)
