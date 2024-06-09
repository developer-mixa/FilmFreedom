from django.test import TestCase
from typing import Iterable
from django.core.exceptions import ValidationError
from cinephile_server.models import Cinema, Film, FilmCinema, Ticket
from tests.data import TEST_CINEMA_ATTRS, TEST_FILM_ATTRS, TEST_URL_IMAGE
from datetime import datetime

def create_model_test(model_class, valid_attrs: dict, bunch_of_invalid_attrs: Iterable = None):
    class ModelTest(TestCase):
        def test_unsuccessful_creation(self):
            if bunch_of_invalid_attrs:
                for invalid_attrs in bunch_of_invalid_attrs:
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
    {'name' : 'test', 'description': 'test', 'rating': 1000.1231, 'url_image': TEST_URL_IMAGE},
    {'name' : 'test', 'description': 'test', 'rating': 6.0, 'url_image': TEST_URL_IMAGE},
    {'name' : 'test', 'description': 'test', 'rating': -1, 'url_image': TEST_URL_IMAGE},
    {'name' : None, 'description': None, 'rating': None, 'url_image': None},
)

time = datetime.now().time()

def get_valid_ticket_attrs(film_cinema):
    return {
            'time' : time,
            'place' : 'some place',
            'price': 100,
            'film_cinema': film_cinema,
        }

def get_invalid_ticket_attrs(film_cinema):
    return (
            {'time' : time, 'place': 'test', 'film_cinema': film_cinema},
            {'time' : time, 'place': 'test', 'film_cinema': film_cinema},
            {'time' : None, 'place': None, 'film_cinema': None},
        )


# tests

CinemaModelTest = create_model_test(Cinema, TEST_CINEMA_ATTRS, cinema_invalid_attrs)
FilmModelTest = create_model_test(Film, TEST_FILM_ATTRS, film_invalid_attrs)

class TicketModelTest(TestCase):

    def setUp(self) -> None:
        created_cinema = Cinema.objects.create(**TEST_CINEMA_ATTRS)
        created_film = Film.objects.create(**TEST_FILM_ATTRS)
        self.film_cinema = FilmCinema.objects.create(film=created_film, cinema=created_cinema)

    def test_unsuccessful_creation(self):
        for invalid_attrs in get_invalid_ticket_attrs(self.film_cinema):
            with self.assertRaises(ValidationError):
                self.try_save(invalid_attrs)
    
    def test_successful_creation(self):
        self.try_save(get_valid_ticket_attrs(self.film_cinema))
    
    def try_save(self, attrs):
        instance = Ticket(**attrs)
        instance.full_clean()
        instance.save()
