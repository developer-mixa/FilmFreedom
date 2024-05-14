from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework import status
from tests.utils import make_simple_test, WithAuthTest
from tests.data import TEST_CINEMA_ATTRS, TEST_FILM_ATTRS
from cinephile_server.models import Cinema, Film, Ticket, FilmCinema
from django.utils import timezone

CinemaViewSetTest = make_simple_test(Cinema, '/rest/cinemas/', TEST_CINEMA_ATTRS)
FilmViewSetTest = make_simple_test(Film, '/rest/films/', TEST_FILM_ATTRS)

class AuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_user(self):
        data = {
            'username': 'testuser2',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }

        #test registration
        response = self.client.post('/accounts/register', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #test sign-in
        response = self.client.post('/api-token-auth/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #test sign-in with wrong password
        data['password'] = 'wrong_password'
        response = self.client.post('/api-token-auth/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class FilmCinemaTest(WithAuthTest):
    def manage(self, user: User, token: Token, put_status: int, delete_status: int):
        self.client.force_authenticate(user=user, token=token)
        url = '/rest/film_cinemas/'

        film = Film.objects.create(**TEST_FILM_ATTRS)
        cinema = Cinema.objects.create(**TEST_CINEMA_ATTRS)

        film_cinema_attrs = {'film': film, 'cinema': cinema}
        film_cinema_id = FilmCinema.objects.create(**{'film': film, 'cinema': cinema}).id
        film_cinema_attrs['cinema'] = cinema.id
        film_cinema_attrs['film'] = film.id

        self.client.session.save()

        object_url = f'{url}{film_cinema_id}/'

        # PUT
        response = self.client.put(object_url, film_cinema_attrs)
        self.assertEqual(response.status_code, put_status)

        # DELETE
        response = self.client.delete(object_url)
        self.assertEqual(response.status_code, delete_status)

    def post(self, user, token, post_status):
        self.client.force_authenticate(user=user, token=token)
        url = '/rest/film_cinemas/'

        film = Film.objects.create(**TEST_FILM_ATTRS)
        cinema = Cinema.objects.create(**TEST_CINEMA_ATTRS)

        film_cinema_attrs = {'film': str(film.id), 'cinema': str(cinema.id)}

        # POST
        response = self.client.post(url, film_cinema_attrs)
        self.assertEqual(response.status_code, post_status)

    def test_manage_user(self):
        self.post(self.user, self.user_token, status.HTTP_403_FORBIDDEN)
        self.manage(
            self.user, self.user_token,
            put_status=status.HTTP_403_FORBIDDEN,
            delete_status=status.HTTP_403_FORBIDDEN,
        )

    def test_manage_superuser(self):
        self.post(self.superuser, self.superuser_token, status.HTTP_201_CREATED)
        self.manage(
            self.superuser, self.superuser_token,
            put_status=status.HTTP_200_OK,
            delete_status=status.HTTP_204_NO_CONTENT,
        )

class TicketTest(WithAuthTest):

    def get_ticket_attrs(self):
        film = Film.objects.create(**TEST_FILM_ATTRS)
        cinema = Cinema.objects.create(**TEST_CINEMA_ATTRS)
        film_cinema = FilmCinema.objects.create(**{'film': film, 'cinema': cinema})
        current_time = timezone.now().time()
        ticket_attrs = {'time': current_time, 'place': 'test_place', 'price': 100, 'film_cinema': film_cinema}
        return film_cinema, ticket_attrs

    def manage(self, user: User, token: Token, put_status: int, delete_status: int):
        self.client.force_authenticate(user=user, token=token)
        url = '/rest/tickets/'
        film_cinema, ticket_attrs = self.get_ticket_attrs()
        ticket_id = Ticket.objects.create(**ticket_attrs).id
        ticket_attrs['film_cinema'] = film_cinema.id

        self.client.session.save()

        object_url = f'{url}{ticket_id}/'

        # PUT
        response = self.client.put(object_url, ticket_attrs)
        self.assertEqual(response.status_code, put_status)

        # DELETE
        response = self.client.delete(object_url)
        self.assertEqual(response.status_code, delete_status)
    
    def post(self, user, token, post_status):
        self.client.force_authenticate(user=user, token=token)
        url = '/rest/tickets/'
        film_cinema, ticket_attrs = self.get_ticket_attrs()
        ticket_attrs['film_cinema'] = film_cinema.id
        response = self.client.post(url, ticket_attrs)
        self.assertEqual(response.status_code, post_status)

    def test_manage_user(self):
        self.post(self.user, self.user_token, status.HTTP_201_CREATED)
        self.manage(
            self.user, self.user_token,
            put_status=status.HTTP_200_OK,
            delete_status=status.HTTP_204_NO_CONTENT,
        )

    def test_manage_superuser(self):
        self.post(self.superuser, self.superuser_token, status.HTTP_201_CREATED)
        self.manage(
            self.superuser, self.superuser_token,
            put_status=status.HTTP_200_OK,
            delete_status=status.HTTP_204_NO_CONTENT,
        )
