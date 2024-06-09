"""Module for views with http methods."""


from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect

import cinephile_server.template_names as template
from cinephile_server.models import Ticket

from .pages import booked_tickets_page


def __set_ticket_state(request: WSGIRequest, cancel_ticket=False) -> HttpResponse | HttpResponseRedirect:
    if request.method == 'POST':
        if request.user.is_authenticated:
            ticket = Ticket.objects.get(id=request.GET.get('ticket_id'))
            ticket.user = None if cancel_ticket else request.user
            ticket.save()
        else:
            return redirect(template.LOGIN)
        return booked_tickets_page(request)
    return HttpResponse('Something went wrong...')


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
    return __set_ticket_state(request)


def cancel_ticket(request: WSGIRequest) -> HttpResponse | HttpResponseRedirect:
    """
    Cancel a ticket for a user if they are authenticated.

    This function processes the cancellation request for a ticket identified by its ID passed via GET parameters.
    If the user is authenticated, it cancels the ticket associated with the user and saves the changes.
    Unauthenticated users are redirected to the login page. Upon successful cancellation, the user is redirected
    to the page displaying their cancelled tickets. In case of any errors during the process, a generic error
    message is returned.

    Parameters:
        request (WSGIRequest): The Django HttpRequest object containing details about the incoming HTTP request.

    Returns:
        HttpResponse: Redirects to the page showing cancelled tickets upon successful cancellation or returns
                     a generic error message if something goes wrong.
    """
    return __set_ticket_state(request, cancel_ticket=True)
