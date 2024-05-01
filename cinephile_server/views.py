from django.shortcuts import render

from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer, CinemaSerializer, FilmSerializer, TicketSerializer, FilmCinemaSerializer
from .models import Cinema, Film, Ticket, FilmCinema
from .auth import LoginRequired

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Cinema
class CinemaCreate(LoginRequired, generics.ListCreateAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer

class CinemaUpdateDestroy(LoginRequired, generics.RetrieveUpdateDestroyAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer

# Film
class FilmCreate(LoginRequired, generics.ListCreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

class FilmUpdateDestroy(LoginRequired, generics.RetrieveUpdateDestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

# Ticket
class TicketCreate(LoginRequired, generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketUpdateDestroy(LoginRequired, generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

#FilmCinema
class FilmCinemaCreate(LoginRequired, generics.ListCreateAPIView):
    queryset = FilmCinema.objects.all()
    serializer_class = FilmCinemaSerializer

class FilmCinemaUpdateDestroy(LoginRequired, generics.RetrieveUpdateDestroyAPIView):
    queryset = FilmCinema.objects.all()
    serializer_class = FilmCinemaSerializer


