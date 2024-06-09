"""Module for all forms."""


from typing import Any

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Film, Ticket

FIRST_NAME_MAX_LENGTH = 100
LAST_NAME_MAX_LENGTH = 100
EMAIL_MAX_LENGTH = 200


class FilmForm(forms.ModelForm):
    """Form for film."""

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        cinemas = cleaned_data.get('cinemas')

        if not cinemas:
            cleaned_data['cinemas'] = []
            return cleaned_data

        return cleaned_data

    class Meta:
        model = Film
        fields = '__all__'
        widgets = {
            'rating': forms.NumberInput(attrs={'min': '0', 'max': '5'}),
        }


class TicketForm(forms.ModelForm):
    """Form for ticket."""

    class Meta:
        model = Ticket
        fields = '__all__'


class RegistrationForm(UserCreationForm):
    """Form for registration."""

    first_name = forms.CharField(max_length=FIRST_NAME_MAX_LENGTH, required=True)
    last_name = forms.CharField(max_length=LAST_NAME_MAX_LENGTH, required=True)
    email = forms.EmailField(max_length=EMAIL_MAX_LENGTH, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
