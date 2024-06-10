"""Module for testing models."""


from datetime import datetime, timezone
from typing import Iterable

from django.core.exceptions import ValidationError
from django.test import TestCase

from cinephile_server.models import Address, Cinema, Film, FilmCinema, Ticket
from tests.data import TEST_URL_IMAGE, test_address_attrs, test_film_attrs


def create_model_test(model_class, valid_attrs: dict, bunch_of_invalid_attrs: Iterable = None):
    """Create test for model.

    Args:
        model_class: model which we need to test
        valid_attrs: valid attrs for succsessfuly creating model.
        bunch_of_invalid_attrs: invalid attrs for unsuccsessfuly creating models.

    Returns:
        _type_: _description_
    """
    class ModelTest(TestCase):
        def test_unsuccessful_creation(self):
            if bunch_of_invalid_attrs:
                for invalid_attrs in bunch_of_invalid_attrs:
                    self.check_raises_invalid_attrs(invalid_attrs)

        def check_raises_invalid_attrs(self, invalid_attrs):
            with self.assertRaises(ValidationError):
                self.try_save(invalid_attrs)

        def test_successful_creation(self):
            self.try_save(valid_attrs)

        def try_save(self, attrs):
            instance = model_class(**attrs)
            instance.full_clean()
            instance.save()

    return ModelTest

# prepare data


cinema_invalid_attrs = (
    {'name': '', 'address': 'some valid address', 'url_image': 'TEST_URL_IMAGE'},
    {'name': 'valid name', 'address': 'short', 'url_image': TEST_URL_IMAGE},
    {'name': 'valid_name', 'address': '', 'url_image': TEST_URL_IMAGE},
    {'name': None, 'address': '', 'url_image': None},
)

film_invalid_attrs = (
    {'name': 'test', 'description': 'test', 'rating': 1000.1231, 'url_image': TEST_URL_IMAGE},
    {'name': 'test', 'description': 'test', 'rating': 6.0, 'url_image': TEST_URL_IMAGE},
    {'name': 'test', 'description': 'test', 'rating': -1, 'url_image': TEST_URL_IMAGE},
    {'name': None, 'description': None, 'rating': None, 'url_image': None},
)

film_date = datetime.now(tz=timezone.utc)


def get_valid_ticket_attrs(film_cinema) -> dict:
    """Return valid ticket attrs.

    Args:
        film_cinema: film cinema model for ticket

    Returns:
        dict: valid attrs for creating ticket
    """
    return {
            'film_date': film_date,
            'place': 'some place',
            'film_cinema': film_cinema,
        }


def get_invalid_ticket_attrs(film_cinema) -> tuple[dict]:
    """Return invalid ticket attrs.

    Args:
        film_cinema: film cinema model for ticket

    Returns:
        tuple[dict]: invalid attrs for creating tickets
    """
    return (
            {'film_date': 'asdasdads', 'place': 12, 'film_cinema': film_cinema},
            {'film_date': None, 'place': None, 'film_cinema': None},
        )


# tests

FilmModelTest = create_model_test(Film, test_film_attrs, film_invalid_attrs)


class TicketModelTest(TestCase):
    """Test for ticket."""

    def setUp(self) -> None:
        """Set up things for tests."""
        address = Address.objects.create(**test_address_attrs)
        created_cinema = Cinema.objects.create(name='test', address=address)
        created_film = Film.objects.create(**test_film_attrs)
        self.film_cinema = FilmCinema.objects.create(film=created_film, cinema=created_cinema)

    def test_unsuccessful_creation(self):
        """Test creating attrs with invalid attrs."""
        for invalid_attrs in get_invalid_ticket_attrs(self.film_cinema):
            with self.assertRaises(ValidationError):
                self.try_save(invalid_attrs)

    def test_successful_creation(self):
        """Test creating ticket with valid attrs."""
        self.try_save(get_valid_ticket_attrs(self.film_cinema))

    def try_save(self, attrs):
        """
        Attempt to save a new Ticket instance with the given attributes.

        This method creates a new Ticket instance using the provided attributes,
        performs full validation on the instance to ensure all required fields
        meet their constraints, and then attempts to save the instance to the database.

        Parameters:
            attrs (dict): A dictionary mapping attribute names to their values for creating
                        a new Ticket instance.

        """
        instance = Ticket(**attrs)
        instance.full_clean()
        instance.save()
