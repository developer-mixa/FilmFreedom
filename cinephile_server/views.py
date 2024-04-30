from django.shortcuts import render

from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer, CinemaSerializer, FilmSerializer, TicketSerializer, FilmCinemaSerializer
from .models import Cinema, Film, Ticket, FilmCinema

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Cinema
class CinemaCreate(generics.ListCreateAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer

class CinemaUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer

# Film
class FilmCreate(generics.ListCreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

class FilmUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

# Ticket
class TicketCreate(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

#FilmCinema
class FilmCinemaCreate(generics.ListCreateAPIView):
    queryset = FilmCinema.objects.all()
    serializer_class = FilmCinemaSerializer

class FilmCinemaUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = FilmCinema.objects.all()
    serializer_class = FilmCinemaSerializer
