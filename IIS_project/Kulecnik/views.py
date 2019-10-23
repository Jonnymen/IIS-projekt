from django.shortcuts import render
from django.http import HttpResponse
from .forms import NewTournament_S
from .models import Tournament_S

# Create your views here.

def index(request):
    turnaje = Tournament_S.objects.all()
    return render(request, template_name='Kulecnik/index.html', context={'tur': turnaje})

def addTournament_S(request):

    if request.method == 'GET':
        form = NewTournament_S()
        return render(request, template_name='Kulecnik/addtournaments.html', context={'form':form})
    else:
        title = request.POST['title']
        tournament = Tournament_S(title=title)
        tournament.save()
        return render(request, template_name='Kulecnik/index.html', context=None)