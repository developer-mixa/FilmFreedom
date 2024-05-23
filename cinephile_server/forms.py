from .models import Film, Ticket
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, EmailField
from django.contrib.auth.models import User


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = '__all__'
        widgets = {
            'rating': forms.NumberInput(attrs={'min': '0', 'max': '5'}),
        }


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        widgets = {
            'price': forms.NumberInput(attrs={'min': '0', 'step': 1}),
        }

class RegistrationForm(UserCreationForm):
    first_name = CharField(max_length=100, required=True)
    last_name = CharField(max_length=100, required=True)
    email = EmailField(max_length=200, required=True)


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']