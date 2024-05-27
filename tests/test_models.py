from django.test import TestCase
from typing import Iterable
from django.core.exceptions import ValidationError
from datetime import date, datetime, timezone, timedelta
from django.contrib.auth.models import User
from cinephile_server.models import Cinema, Film, FilmCinema, Ticket
from tests.data import TEST_CINEMA_ATTRS, TEST_FILM_ATTRS, TEST_URL_IMAGE

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

cinema_invalid_attrs = (
    {'name': '*' * 81000, 'address': '', 'url_image': 'TEST_URL_IMAGE'},
    {'name': '', 'address': '', 'url_image': 'TEST_URL_IMAGE'},
    {'name': 'valid name', 'address': 'short', 'url_image': 'TEST_URL_IMAGE'},
    {'name': 'valid_name', 'address': '', 'url_image': 'TEST_URL_IMAGE'},
    {'name': None, 'address': '', 'url_image': None},
)

CinemaModelTest = create_model_test(Cinema, TEST_CINEMA_ATTRS, cinema_invalid_attrs)