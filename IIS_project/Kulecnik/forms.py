from django.forms import ModelForm, Form
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tournament_S

class NewTournament_S(forms.Form):

    title = forms.CharField(max_length=50)

class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta():
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )
        
class LoginForm(forms.Form):

    username = forms.CharField(max_length=40)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    class Meta():
        fields = (
            'username',
            'password'
        )
        labels = {
            'username': 'test',
            'password': 'heslo'
        }