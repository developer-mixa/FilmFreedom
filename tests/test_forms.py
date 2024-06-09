from django.test import TestCase
from cinephile_server.forms import RegistrationForm, FilmForm, TicketForm
from django.contrib.auth.models import User
from tests.data import TEST_URL_IMAGE
from datetime import datetime

valid_data = {
    'username': 'abc',
    'first_name': 'abc',
    'last_name': 'abc',
    'email': 'email@email.com',
    'password1': 'tArAs0ff2005',
    'password2': 'tArAs0ff2005',
}

not_matching_password = valid_data.copy()
not_matching_password['password2'] = 'abc'

invalid_email = valid_data.copy()
invalid_email['email'] = 'abc'

short_password = valid_data.copy()
short_password['password1'] = 'abc'
short_password['password2'] = 'abc'

common_password = valid_data.copy()
common_password['password1'] = 'abcdef123'
common_password['password2'] = 'abcdef123'

class TestRegistrationForm(TestCase):
    def test_valid(self):
        self.assertTrue(RegistrationForm(data=valid_data).is_valid())

    def test_not_matching_passwords(self):
        self.assertFalse(RegistrationForm(data=not_matching_password).is_valid())
        
    def test_short_password(self):
        self.assertFalse(RegistrationForm(data=short_password).is_valid())

    def test_invalid_email(self):
        self.assertFalse(RegistrationForm(data=invalid_email).is_valid())

    def test_common_password(self):
        self.assertFalse(RegistrationForm(data=common_password).is_valid())

    def test_existing_user(self):
        User.objects.create(username=valid_data['username'], password='abc')
        self.assertFalse(RegistrationForm(data=valid_data).is_valid())


def create_dynamic_form_test(form, data, error_field: str):
    class TestForm(TestCase):
        def setUp(self):
            self.form = form
            self.form_data = data.copy()

        def test_valid(self):
            self.assertTrue(self.form(self.form_data).is_valid())
        
        def test_error_field_in_range(self):
            self.form_data[error_field] = -1
            self.assertFalse(self.form(self.form_data).is_valid())
        
        def test_required_fields(self):
            del self.form_data[error_field]
            self.assertFalse(self.form(self.form_data).is_valid())
    return TestForm


film_data = {
    'name' : 'film_name',
    'description' : 'film_description',
    'rating' : 1.00,
    'url_image': TEST_URL_IMAGE,
}

TestFilmForm = create_dynamic_form_test(FilmForm, film_data, 'rating')