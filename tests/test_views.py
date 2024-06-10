"""Module for testing views."""


from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client as TestClient
from django.urls import reverse
from rest_framework import status

from cinephile_server.models import Film
from tests.data import test_film_attrs

# helper methods


def test_simple_page(url: str, template: str) -> TestCase:
    """Test simple page without entities.

    Args:
        url (str): url for page
        template (str): your template

    Returns:
        TestCase: Test Case
    """
    class PageTest(TestCase):
        def test_success_page(self):
            self.client = TestClient()
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTemplateUsed(response, template)
    return PageTest


def test_page_with_entity(path_name: str, template: str, model, attrs) -> TestCase:
    """Test page with some entity.

    Args:
        path_name: path name for reverse
        template: your template
        model: model which we creates
        attrs: attrs for creating model

    Returns:
        TestCase: Test case
    """
    class PageTest(TestCase):
        def test_success_page(self):
            self.client = TestClient()
            created_model = model.objects.create(**attrs)
            url = reverse(path_name, kwargs={'pk': created_model.id})
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTemplateUsed(response, template)
    return PageTest

# tests


CINEMAS_PAGE_TEST = test_simple_page(url='/cinemas/', template='cinemas.html')
FILMS_PAGE_TEST = test_simple_page(url='/films/', template='films.html')
HOME_PAGE_TEST = test_simple_page(url='/', template='index.html')
PROFILE_PAGE_TEST = test_simple_page(url='/accounts/profile/', template='profile.html')
LOGIN_PAGE_TEST = test_simple_page(url='/login/', template='registration/login.html')
PASSWORD_RESET_PAGE_TEST = test_simple_page(
    url='/accounts/password_reset/',
    template='registration/password_reset_form.html',
)

DETAIL_FILM_TEST = test_page_with_entity(
    path_name='film',
    template='film_detail.html',
    model=Film,
    attrs=test_film_attrs,
)


class TicketPageTest(TestCase):
    """Test for ticket page."""

    def setUp(self) -> None:
        """Set up things for testing things."""
        self.client = TestClient()

    def test_page_without_auth(self):
        """Test ticket page without auth user."""
        response = self.client.get('/tickets/')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTemplateNotUsed('booked_tickets.hmtl')
        self.assertTemplateUsed('profile.html')

    def test_page_with_auth(self):
        """Test ticket page with auth user."""
        user = User.objects.create_user(username='test', password='test')
        self.client.force_login(user)
        response = self.client.get('/tickets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed('booked_tickets.hmtl')
