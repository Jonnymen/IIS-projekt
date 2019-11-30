from django.forms import ModelForm, Form
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .models import Tournament_S, Tournament_T, Profile, Team

class NewTournament_S(forms.Form):

    title = forms.CharField(max_length=50)

class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta():
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
        )
        labels = {
            "email": _("E-mail*"),
            "first_name": "Křestní jméno",
            "last_name": "Příjmení",
            "password1": "Heslo*",
            "password2": "Potvrďte heslo*",
            "username": "Uživatelské jméno*",
        }
        widgets = {
            "email": forms.EmailInput(attrs={'placeholder': '2017-10-20', 'rows':1, 'cols':15}),
        }

class EditProfileForm(UserChangeForm):

    class Meta():
        model = User
        fields = (
            'first_name',
            'last_name',
            'email'
        )
        labels = {
            "first_name": "Křestní jméno",
            "last_name": "Příjmení",
            "email": "Email",
        }

class EditPicture(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)

class EditLogo(forms.ModelForm):
    logo = forms.ImageField()
    class Meta:
        model = Team
        fields = ('logo',)

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

class AddTournamentFormS(forms.ModelForm):

    class Meta():
        model = Tournament_S
        fields = (
            'title',
            'start_date',
            'end_date',
            'entry_fee',
            'place',
            'capacity',
            'reg_deadline',
            'description'
        )
        widgets = {
            'start_date': forms.TextInput(attrs={'placeholder': '2017-10-20', 'rows':1, 'cols':15}),
            'description': forms.Textarea(attrs={'placeholder': 'Zde přidejte popis...', 'rows':4, 'cols':28}),
            'title': forms.TextInput(attrs={'rows':1, 'cols':15}),
            'end_date': forms.TextInput(attrs={'placeholder': '2017-10-21', 'rows':1, 'cols':15}),
            'entry_fee': forms.TextInput(attrs={'placeholder': 'Kč', 'rows':1, 'cols':15}),
            'place': forms.TextInput(attrs={'rows':1, 'cols':15}),
            'capacity': forms.TextInput(attrs={'placeholder': '4/8/16/32', 'rows':1, 'cols':15}),
            'reg_deadline': forms.TextInput(attrs={'placeholder': '2017-10-15', 'rows':1, 'cols':15}),
        }
        labels = {
            "title": "Název",
            "start_date": "Začátek",
            "end_date": "Konec",
            "entry_fee": "Startovné",
            "place": "Místo",
            "capacity": "Kapacita",
            "description": "Popis",
            "reg_deadline": "Konec registrací",
        }


class AddTournamentFormT(forms.ModelForm):
    class Meta():
        model = Tournament_T
        fields = (
            'title',
            'start_date',
            'end_date',
            'entry_fee',
            'place',
            'capacity',
            'reg_deadline',
            'description'
        )
        widgets = {
            'start_date': forms.TextInput(attrs={'placeholder': '2017-10-20', 'rows':1, 'cols':15}),
            'description': forms.Textarea(attrs={'placeholder': 'Zde přidejte popis...', 'rows':4, 'cols':28}),
            'title': forms.TextInput(attrs={'rows':1, 'cols':15}),
            'end_date': forms.TextInput(attrs={'placeholder': '2017-10-21', 'rows':1, 'cols':15}),
            'entry_fee': forms.TextInput(attrs={'placeholder': 'Kč', 'rows':1, 'cols':15}),
            'place': forms.TextInput(attrs={'rows':1, 'cols':15}),
            'capacity': forms.TextInput(attrs={'placeholder': '4/8/16/32', 'rows':1, 'cols':15}),
            'reg_deadline': forms.TextInput(attrs={'placeholder': '2017-10-15', 'rows':1, 'cols':15}),
        }
        labels = {
            "title": "Název",
            "start_date": "Začátek",
            "end_date": "Konec",
            "entry_fee": "Startovné",
            "place": "Místo",
            "capacity": "Kapacita",
            "description": "Popis",
            "reg_deadline": "Konec registrací",
        }

class NewTeamForm(forms.ModelForm):

    class Meta():
        model = Team
        fields = (
            'name',
        )
        labels = {
            "name": "Jméno týmu:",
        }
