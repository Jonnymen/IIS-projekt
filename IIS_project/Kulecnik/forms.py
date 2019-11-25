from django.forms import ModelForm, Form
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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

class EditProfileForm(UserChangeForm):

    class Meta():
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
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

class AddTournamentForm(forms.ModelForm):
    '''
    title = forms.CharField(max_length=60)
    start_date = forms.DateField(input_formats=['%d/%m/%Y'])
    end_date = forms.DateField(input_formats=['%d/%m/%Y'])
    entry_fee = forms.IntegerField()
    place = forms.CharField(max_length=100)
    capacity = forms.IntegerField()
    description = forms.TextInput()
    reg_deadline = forms.DateField(input_formats=['%d/%m/%Y'])
    '''
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
            'start_date': forms.TextInput(attrs={'rows':1, 'cols':15}),
            'description': forms.Textarea(attrs={'placeholder': 'Zde přidejte popis...', 'rows':4, 'cols':28}),
            'title': forms.TextInput(attrs={'rows':1, 'cols':15}),
            'end_date': forms.TextInput(attrs={'rows':1, 'cols':15}),
            'entry_fee': forms.TextInput(attrs={'rows':1, 'cols':15}),
            'place': forms.TextInput(attrs={'rows':1, 'cols':15}),
            'capacity': forms.TextInput(attrs={'rows':1, 'cols':15}),
            'reg_deadline': forms.TextInput(attrs={'rows':1, 'cols':15}),
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
