"""Module for all pages."""


from uuid import UUID

from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Prefetch
from django.shortcuts import HttpResponse, redirect, render

import cinephile_server.template_names as template
from cinephile_server.forms import RegistrationForm
from cinephile_server.models import Cinema, Film, Ticket


def __generate_html_page(request, template_name, context=None, extension='html') -> HttpResponse:
    if context is None:
        context = {}
    return render(request, f'{template_name}.{extension}', context)


def __get_tickets_by_film_cinema(model: Film | Cinema) -> list[Ticket]:
    film_cinemas = model.filmcinema_set.all()
    all_tickets = Ticket.objects.prefetch_related(
        Prefetch('film_cinema', queryset=film_cinemas, to_attr='film_cinemas'),
    )
    tickets = []
    for ticket in all_tickets:
        ids = (ticket.film_cinema.film.id, ticket.film_cinema.cinema.id)
        if model.id in ids:
            tickets.append(ticket)
    return tickets


def __generate_detail_page(request, model, pk) -> HttpResponse:
    got_model = model.objects.get(id=pk)
    tickets = __get_tickets_by_film_cinema(got_model)
    return __generate_html_page(request, template.FILM_DETAILS, {'film': got_model, 'tickets': tickets})

# pages


def main_page(request) -> HttpResponse:
    """Return main page.

    Args:
        request (WSGIRequest): django request

    Returns:
        HttpResponse: main page
    """
    return __generate_html_page(request, template.INDEX)


def films_page(request: WSGIRequest) -> HttpResponse:
    """Return films page.

    Args:
        request (WSGIRequest): django request

    Returns:
        HttpResponse: films page
    """
    return __generate_html_page(request, template.FILMS, {template.FILMS: Film.objects.all()})


def cinemas_page(request: WSGIRequest) -> HttpResponse:
    """Return cinemas page.

    Args:
        request (WSGIRequest): django request

    Returns:
        HttpResponse: cinemas page
    """
    return __generate_html_page(request, template.CINEMAS, {template.CINEMAS: Cinema.objects.all()})


def film_detail_page(request: WSGIRequest, pk) -> HttpResponse:
    """Return film detail page.

    Args:
        request (WSGIRequest): django request
        pk (_type_): film detail primary key

    Returns:
        HttpResponse: film detail page
    """
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
