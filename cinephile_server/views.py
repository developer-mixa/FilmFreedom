from django.shortcuts import render, redirect, HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from rest_framework import generics
from django.contrib.auth.models import User
from django.http import HttpRequest
from .serializers import UserSerializer, CinemaSerializer, FilmSerializer, TicketSerializer, FilmCinemaSerializer
from .models import Cinema, Film, Ticket, FilmCinema
from .auth import LoginRequired, LoginAdminRequired
from .forms import RegistrationForm

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

# helpers

def generate_page(request, template_name, context=None):
    if context is None:
        context = {}
    return render(request, template_name, context)

def get_tickets_by_cinema(cinema: Cinema) -> list[Ticket]:
    film_cinemas = []
    tickets = []
    for film in cinema.films.all():
        try:
            film_cinema = FilmCinema.objects.get(film=film, cinema=cinema)
            film_cinemas.append(film_cinema)
        except FilmCinema.DoesNotExist:
            continue
    for film_cinema in film_cinemas:
        try:
            ticket = Ticket.objects.get(film_cinema=film_cinema)
            tickets.append(ticket)
        except Ticket.DoesNotExist:
            continue
    return tickets

# pages

def main_page(request):
    return generate_page(request, 'index.html')

def films_page(request):
    return generate_page(request, 'films.html', {'films': Film.objects.all()})

def cinemas_page(request):
    return generate_page(request, 'cinemas.html', {'cinemas': Cinema.objects.all()})

def film_detail_page(request, pk):
    film = Film.objects.get(id=pk)
    return generate_page(request, 'film_detail.html', {'film': film})

def cinema_detail_page(request, pk):
    cinema = Cinema.objects.get(id=pk)
    tickets = get_tickets_by_cinema(cinema)
    return generate_page(request, 'cinema_detail.html', {'cinema': cinema, 'tickets': tickets})

def booked_tickets_page(request: WSGIRequest):
    if request.user.is_authenticated:
        user = request.user
        tickets = Ticket.objects.filter(user=user)
        return generate_page(request, 'booked_tickets.html', {'tickets': tickets})
    return redirect('/accounts/profile/')

def profile_page(request: WSGIRequest):
    return generate_page(request, 'profile.html', {'user': request.user})

def register_page(request: WSGIRequest):
    errors = ''
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            return redirect('')
        else:
            errors = form.errors
    else:
        form = RegistrationForm()
    return render(
        request,
        'registration/register.html',
        {'form': form, 'errors': errors},
    )

# queries

def book_ticket(request: WSGIRequest):
    if request.method == 'POST':
        if request.user.is_authenticated:
            ticket_id = request.GET.get('ticket_id')
            print(ticket_id)
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.user = request.user
            ticket.save()
        else:
            return redirect('login/')
        return booked_tickets_page(request)
    return HttpResponse('Something went wrong...')