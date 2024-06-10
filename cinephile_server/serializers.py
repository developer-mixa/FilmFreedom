"""Module for serializers."""


from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Address, Cinema, Film, FilmCinema, Ticket

ALL = '__all__'


class UserSerializer(HyperlinkedModelSerializer):
    """Serializer for the User model."""

    class Meta:
        """Settings for user serializer."""

        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data) -> User:
        """Create a new user and associated token.

        Args:
            validated_data: validated data for user

        Returns:
            User: created user
        """
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class CinemaSerializer(HyperlinkedModelSerializer):
    """Serializer for the Cinema model."""

    class Meta:
        """Settings for cinema serializer."""

        model = Cinema
        fields = ALL


class FilmSerializer(HyperlinkedModelSerializer):
    """Serializer for the Film model."""

    class Meta:
        """Settings for film serializer."""

        model = Film
        fields = ALL


class TicketSerializer(HyperlinkedModelSerializer):
    """Serializer for the Ticket model."""

    class Meta:
        """Settings for ticket serializer."""

        model = Ticket
        fields = ALL


class FilmCinemaSerializer(HyperlinkedModelSerializer):
    """Serializer for the FilmCinema model."""

    class Meta:
        """Settings for film_cinema serializer."""

        model = FilmCinema
        fields = ALL


class AddressSerializer(HyperlinkedModelSerializer):
    """Serializer for the Address model."""

    class Meta:
        """Settings for address serializer."""

        model = Address
        fields = ALL
