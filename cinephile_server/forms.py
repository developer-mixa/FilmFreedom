from .models import Film, Ticket
from django import forms

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