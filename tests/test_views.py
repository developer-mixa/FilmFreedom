from django.test.client import Client as TestClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from cinephile_server.models import Cinema, Film
from tests.data import TEST_CINEMA_ATTRS, TEST_FILM_ATTRS
from django.contrib.auth.models import User

# helper methods

def test_simple_page(url, template):
    class PageTest(TestCase):
        def test_success_page(self):
            self.client = TestClient()
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTemplateUsed(response, template)
    return PageTest

def test_page_with_entity(path_name, template, model, attrs):
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
PASSWORD_RESET_PAGE_TEST = test_simple_page(url='/accounts/password_reset/', template='registration/password_reset_form.html')


DETAIL_CINEMA_TEST = test_page_with_entity(
    path_name='cinema',
    template='cinema_detail.html',
    model=Cinema,
    attrs=TEST_CINEMA_ATTRS
)

DETAIL_FILM_TEST = test_page_with_entity(
    path_name='film',
    template='film_detail.html',
    model=Film,
    attrs=TEST_FILM_ATTRS
)

class TicketPageTest(TestCase):

    def setUp(self) -> None:
        self.client = TestClient()

    def test_page_without_auth(self):
        response = self.client.get('/tickets/')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTemplateNotUsed('booked_tickets.hmtl')
        self.assertTemplateUsed('profile.html')

    def test_page_with_auth(self):
        user = User.objects.create_user(username='test', password='test')       
        self.client.force_login(user)
        response = self.client.get('/tickets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed('booked_tickets.hmtl')
