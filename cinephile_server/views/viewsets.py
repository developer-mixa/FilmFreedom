"""Module for all viewsets."""


from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet

import cinephile_server.serializers as serializers
from cinephile_server.auth import LoginAdminRequired, LoginRequired
from cinephile_server.models import Cinema, Film, FilmCinema, Ticket, Address


class UserViewSet(ModelViewSet):
    """ViewSet for users."""

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class CinemaViewSet(LoginAdminRequired, ModelViewSet):
    """ViewSet for cinemas."""

    queryset = Cinema.objects.all()
    serializer_class = serializers.CinemaSerializer


class FilmViewSet(LoginAdminRequired, ModelViewSet):
    """ViewSet for films."""

    queryset = Film.objects.all()
    serializer_class = serializers.FilmSerializer


class FilmCinemaViewSet(LoginAdminRequired, ModelViewSet):
    """ViewSet for films and cinemas."""

    queryset = FilmCinema.objects.all()
    serializer_class = serializers.FilmCinemaSerializer


class TicketViewSet(LoginRequired, ModelViewSet):
    """ViewSet for tickets."""

    queryset = Ticket.objects.all()
    serializer_class = serializers.TicketSerializer


class AddressViewSet(LoginRequired, ModelViewSet):
    """ViewSet for addresses."""

    queryset = Address.objects.all()
    serializer_class = serializers.AddressSerializer