"""Module for testing forms."""


from django.contrib.auth.models import User
from django.test import TestCase

from cinephile_server.forms import FilmForm, RegistrationForm
from tests.data import TEST_URL_IMAGE

valid_data = {
    'username': 'username',
    'first_name': 'some first name',
    'last_name': 'some last name',
    'email': 'email@email.com',
    'password1': 'tArAs0ff2005',
    'password2': 'tArAs0ff2005',
}

not_matching_password = valid_data.copy()
not_matching_password['password2'] = 'sht'

invalid_email = valid_data.copy()
invalid_email['email'] = 'invalidemail'

short_password = valid_data.copy()
short_password['password1'] = 'abc'
short_password['password2'] = 'abc'

common_password = valid_data.copy()
common_password['password1'] = 'abcdef123'
common_password['password2'] = 'abcdef123'


class TestRegistrationForm(TestCase):
    """Test for registration form."""

    def test_valid(self):
        """Test for valid data."""
        self.assertTrue(RegistrationForm(data=valid_data).is_valid())

    def test_not_matching_passwords(self):
        """Test for not matching passwords."""
        self.assertFalse(RegistrationForm(data=not_matching_password).is_valid())

    def test_short_password(self):
        """Test for short password."""
        self.assertFalse(RegistrationForm(data=short_password).is_valid())

    def test_invalid_email(self):
        """Test for invalid email."""
        self.assertFalse(RegistrationForm(data=invalid_email).is_valid())

    def test_common_password(self):
        """Test for common passwords."""
        self.assertFalse(RegistrationForm(data=common_password).is_valid())

    def test_existing_user(self):
        """Test for existing user."""
        User.objects.create(username=valid_data['username'], password=valid_data['password1'])
        self.assertFalse(RegistrationForm(data=valid_data).is_valid())


def create_dynamic_form_test(form, test_data, error_field: str):
    """Create form test.

    Args:
        form: form which you test
        test_data: data for testing form
        error_field: field which be wrong

    Returns:
        _type_: _description_
    """
    class TestForm(TestCase):
        """Class for testing form."""

        def setUp(self):
            self.form = form
            self.form_data = test_data.copy()

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
    'name': 'film_name',
    'description': 'film_description',
    'rating': 1,
    'url_image': TEST_URL_IMAGE,
}

TestFilmForm = create_dynamic_form_test(FilmForm, film_data, 'rating')
