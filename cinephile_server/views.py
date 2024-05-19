from django.shortcuts import render

from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer, CinemaSerializer, FilmSerializer, TicketSerializer, FilmCinemaSerializer
from .models import Cinema, Film, Ticket, FilmCinema
from .auth import LoginRequired, LoginAdminRequired

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Cinema
class CinemaCreate(LoginAdminRequired, generics.ListCreateAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer

class CinemaUpdateDestroy(LoginAdminRequired, generics.RetrieveUpdateDestroyAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer

# Film
class FilmCreate(LoginAdminRequired, generics.ListCreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

class FilmUpdateDestroy(LoginAdminRequired, generics.RetrieveUpdateDestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

#FilmCinema
class FilmCinemaCreate(LoginAdminRequired, generics.ListCreateAPIView):
    queryset = FilmCinema.objects.all()
    serializer_class = FilmCinemaSerializer

class FilmCinemaUpdateDestroy(LoginAdminRequired, generics.RetrieveUpdateDestroyAPIView):
    queryset = FilmCinema.objects.all()
    serializer_class = FilmCinemaSerializer

# Ticket
class TicketCreate(LoginRequired, generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketUpdateDestroy(LoginRequired, generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

def generate_page(request, template_name, context=None):
    if context is None:
        context = {}
    return render(request, template_name, context)

def main_page(request):
    return generate_page(request, 'index.html')

def films_page(request):
    return generate_page(request, 'films.html', {'films': Film.objects.all()})

def cinemas_page(request):
    return generate_page(request, 'cinemas.html', {'cinemas': Film.objects.all()})

def film_detail_page(request, pk):
    film = Film.objects.get(id=pk)
    return generate_page(request, 'film_detail.html', {'film': film})
