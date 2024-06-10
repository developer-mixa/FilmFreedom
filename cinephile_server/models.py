"""Module for models."""


from uuid import uuid4

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class UUIDMixin(models.Model):
    """Class which adds id field."""

    id = models.UUIDField(primary_key=True, blank=True, editable=False, default=uuid4)

    class Meta:
        abstract = True


MAX_URL_LENGTH = 190000
TICKET_MAX_LENGTH = 256
CINEMA_NAME_MAX_LENGTH = 80
FILM_NAME_MAX_LENGTH = 80
DESCRIPTION_MAX_LENGTH = 1024
ADDRESS_MAX_LENGTH = 1024


class UrlMixin(models.Model):
    """Class which adds url field."""

    url_image = models.TextField(max_length=MAX_URL_LENGTH, null=True, default=None)

    class Meta:
        abstract = True


def check_positive(number: int | float):
    """Check the number is positive.

    Args:
        number (int | float): your number

    Raises:
        ValidationError: Error for django admin
    """
    if number < 0:
        raise ValidationError(
            'number must be more than 0!',
            params={'number': number},
            )


def check_rating(rating: float):
    """Check that rating is more 5.

    Args:
        rating (float): your rating

    Raises:
        ValidationError: Error for django admin
    """
    if rating > 5:
        raise ValidationError(
            'rating must be <= 5!',
            params={'number': rating},
            )


def check_address_len(address: str):
    """Check that address is less 11.

    Args:
        address (str): your address

    Raises:
        ValidationError: Error for django admin
    """
    if len(address) <= 10:
        raise ValidationError(
            'addres cannot be less than 10!',
            params={'address': address},
        )

def check_body(body: str):
    if not body.isdigit() and len(body) > 1:
        raise ValidationError(
            'Body can only contain one letter',
            params={'body': body}
        )
    if body.isdigit():
        check_positive(int(body))


class Address(UUIDMixin):
    """Model for address"""
    city_name = models.TextField(max_length=256, null=False, blank=False)
    street_name = models.TextField(max_length=256, null=False, blank=False)
    house_number = models.IntegerField(null=False, blank=False, validators=[check_positive])
    apartment_number = models.IntegerField(null=True, blank=True, validators=[check_positive])
    body = models.TextField(null=True, blank=True, validators=[check_body])


class Cinema(UUIDMixin, UrlMixin):
    """Module for cinema."""

    name = models.TextField(max_length=CINEMA_NAME_MAX_LENGTH, null=False, blank=False)
    address = models.ForeignKey(Address, verbose_name='address', on_delete=models.CASCADE)
    films = models.ManyToManyField('Film', through='FilmCinema', verbose_name='Films')

    def __str__(self) -> str:
        return f'name={self.name} address={self.address}'

    class Meta:
        db_table = '"api_data"."cinema"'


class Film(UUIDMixin, UrlMixin):
    """Module for film."""

    name = models.TextField(max_length=FILM_NAME_MAX_LENGTH, null=False, blank=False)
    description = models.TextField(max_length=DESCRIPTION_MAX_LENGTH, null=False, blank=False)
    rating = models.DecimalField(decimal_places=1, max_digits=2, null=False, validators=[check_positive, check_rating])

    cinemas = models.ManyToManyField('Cinema', through='FilmCinema', verbose_name='cinemas', blank=True)

    def __str__(self) -> str:
        return f'name={self.name} rating={self.rating}'

    class Meta:
        db_table = '"api_data"."film"'


class FilmCinema(UUIDMixin):
    """Module for film with cinema."""

    cinema = models.ForeignKey(Cinema, verbose_name='cinema', on_delete=models.CASCADE)
    film = models.ForeignKey(Film, verbose_name='film', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'film={self.film} cinema={self.cinema}'

    class Meta:
        db_table = '"api_data"."film_to_cinema"'
        unique_together = (('cinema', 'film'),)


class Ticket(UUIDMixin):
    """Model for ticket."""

    time = models.TimeField(null=False)
    place = models.TextField(max_length=TICKET_MAX_LENGTH, null=False, blank=False)

    film_cinema = models.OneToOneField(FilmCinema, on_delete=models.CASCADE, blank=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f'place={self.place} filmcinema={self.film_cinema}'

    class Meta:
        db_table = '"api_data"."ticket"'
