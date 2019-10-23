from django.forms import ModelForm, Form
from django import forms
from .models import Tournament_S

class NewTournament_S(Form):

    title = forms.CharField(max_length=50)
        