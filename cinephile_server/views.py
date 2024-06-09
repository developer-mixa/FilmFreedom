from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Prefetch
from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect, render
from rest_framework.viewsets import ModelViewSet

import cinephile_server.template_names as template

from .auth import LoginAdminRequired, LoginRequired
from .forms import RegistrationForm
from .models import Cinema, Film, FilmCinema, Ticket
from .serializers import (CinemaSerializer, FilmCinemaSerializer,
                          FilmSerializer, TicketSerializer, UserSerializer)

from uuid import UUID

# viewsets


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CinemaViewSet(LoginAdminRequired, ModelViewSet):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


class FilmViewSet(LoginAdminRequired, ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer


class FilmCinemaViewSet(LoginAdminRequired, ModelViewSet):
    queryset = FilmCinema.objects.all()
    serializer_class = FilmCinemaSerializer


class TicketViewSet(LoginRequired, ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

# helpers


def __generate_html_page(request, template_name, context=None, extension='html') -> HttpResponse:
    if context is None:
        context = {}
    return render(request, f'{template_name}.{extension}', context)


def __get_tickets_by_film_cinema(model: Film | Cinema) -> list[Ticket]:
    film_cinemas = model.filmcinema_set.all()
    all_tickets = Ticket.objects.prefetch_related(
        Prefetch('film_cinema', queryset=film_cinemas, to_attr='film_cinemas')
    )
    tickets = []
    for ticket in all_tickets:
        if model.id in (ticket.film_cinema.film.id, ticket.film_cinema.cinema.id):
            tickets.append(ticket)
    return tickets

def __generate_detail_page(request, model, pk):
    got_model = model.objects.get(id=pk)
    tickets = __get_tickets_by_film_cinema(got_model)
    return __generate_html_page(request, template.FILM_DETAILS, {'film': got_model, 'tickets': tickets})

# pages


def main_page(request):
    return __generate_html_page(request, template.INDEX)


def films_page(request: WSGIRequest):
    return __generate_html_page(request, template.FILMS, {template.FILMS: Film.objects.all()})


def cinemas_page(request: WSGIRequest):
    return __generate_html_page(request, template.CINEMAS, {template.CINEMAS: Cinema.objects.all()})


def film_detail_page(request: WSGIRequest, pk):
    return __generate_detail_page(request, Film, pk)


def cinema_detail_page(request: WSGIRequest, pk: UUID) -> HttpResponse:
    """Return cinema detail page.

    Args:
        request (WSGIRequest): django request
        pk (UUID): cinema id

    Returns:
        HttpResponse: cinema detail page
    """
    cinema = Cinema.objects.get(id=pk)
    tickets = __get_tickets_by_film_cinema(cinema)
    return __generate_html_page(request, template.CINEMA_DETAILS, {'cinema': cinema, 'tickets': tickets})


def booked_tickets_page(request: WSGIRequest):
    """
    Display a page showing all booked tickets for the currently authenticated user.

    This function checks if the user is authenticated. If so, it retrieves all tickets associated with the user
    from the database and passes them to a template for rendering. If the user is not authenticated, it redirects
    them to the profile page, assuming they would need to log in to see their booked tickets.

    Parameters:
        request (WSGIRequest): The Django HttpRequest object containing details about the incoming HTTP request.

    Returns:
        HttpResponse: Generates and returns an HTML page displaying the user's booked tickets or redirects to the
                      profile page if the user is not authenticated.
    """
    if request.user.is_authenticated:
        user = request.user
        tickets = Ticket.objects.filter(user=user)
        return __generate_html_page(request, template.BOOKED_TICKETS, {'tickets': tickets})
    return redirect(template.PROFILE)


def profile_page(request: WSGIRequest) -> HttpResponse:
    """Return profile page.

    Args:
        request (WSGIRequest): django request

    Returns:
        HttpResponse: profile page
    """
    return __generate_html_page(request, template.PROFILE, {'user': request.user})


def register_page(request: WSGIRequest):
    """
    Handle the registration page for new users.

    This function displays the registration form to users and processes submitted forms. If the form is valid,
    it creates a new user account and saves it to the database. Unsaved errors from the form validation are captured
    and displayed to the user. Upon successful registration, the user is redirected to a specified page. If the request
    method is not POST, it simply renders the registration form.

    Parameters:
        request (WSGIRequest): The Django HttpRequest object containing details about the incoming HTTP request.

    Returns:
        HttpResponse: Generates and returns an HTML page with the registration form and any validation errors.
                      Redirects to a specified URL upon successful registration.
    """
    errors = ''
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user: User = form.save()
            user.save()
            return redirect('')
        else:
            errors = form.errors
    else:
        form = RegistrationForm()
    return __generate_html_page(
        request,
        template.REGISTER,
        {'form': form, 'errors': errors},
    )

# queries


def book_ticket(request: WSGIRequest) -> HttpResponse | HttpResponseRedirect:
    """
    Books a ticket for a user if they are authenticated.

    This function handles the booking process for a ticket identified by a ticket ID passed via GET parameters.
    If the user is authenticated, it assigns the ticket to the user and saves the change. Otherwise, it redirects
    unauthenticated users to the login page. After successfully booking a ticket, it redirects the user to the
    booked tickets page. If any error occurs during this process, it returns a generic error message.

    Parameters:
        request (WSGIRequest): The Django HttpRequest object containing details about the incoming HTTP request.

    Returns:
        HttpResponse: Redirects to the booked tickets page upon successful booking or returns a generic error message
                     if something goes wrong.
    """
    if request.method == 'POST':
        if request.user.is_authenticated:
            ticket = Ticket.objects.get(id=request.GET.get('ticket_id'))
            ticket.user = request.user
            ticket.save()
        else:
            return redirect(template.LOGIN)
        return booked_tickets_page(request)
    return HttpResponse('Something went wrong...')
