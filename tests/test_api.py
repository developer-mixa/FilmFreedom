"""Module for testing api."""


from datetime import datetime, timezone

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from cinephile_server.models import Address, Cinema, Film, FilmCinema, Ticket
from tests.data import test_address_attrs, test_film_attrs
from tests.utils import WithAuthTest, create_hyperlink, make_simple_test

FilmViewSetTest = make_simple_test(Film, '/rest/film/', test_film_attrs)
AddressViewSetTest = make_simple_test(Address, '/rest/address/', test_address_attrs)


class AuthTest(TestCase):
    """Test for authenfication."""

    def setUp(self):
        """Set up start things for tests."""
        self.client = APIClient()

    def test_auth_user(self):
        """Test authenfication for user."""
        auth_data = {
            'username': 'testuser2',
            'email': 'testuser@example.com',
            'password': 'testpassword',
        }

        # test registration
        response = self.client.post('/rest/user/', auth_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # test sign-in
        response = self.client.post('/api-token-auth/', auth_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test sign-in with wrong password
        auth_data['password'] = 'wrong_password'
        response = self.client.post('/api-token-auth/', auth_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class FilmCinemaTest(WithAuthTest):
    """Class for testing film cinema."""

    def manage(self, user: User, token: Token, put_status: int, delete_status: int):
        """Test put and delete methods.

        Args:
            user: user to authenticate
            token: token to authenticate
            put_status : status which asserts for put
            delete_status (int): status which asserts for delete
        """
        self.client.force_authenticate(user=user, token=token)
        url = '/rest/film_cinema/'

        film = Film.objects.create(**test_film_attrs)
        address = Address.objects.create(**test_address_attrs)
        cinema = Cinema.objects.create(name='test', address=address)

        film_cinema_attrs = {'film': film, 'cinema': cinema}
        film_cinema_id = FilmCinema.objects.create(film=film, cinema=cinema).id
        film_cinema_attrs['cinema'] = create_hyperlink(cinema.id, 'cinema')
        film_cinema_attrs['film'] = create_hyperlink(film.id, 'film')

        self.client.session.save()

        object_url = f'{url}{film_cinema_id}/'

        # PUT
        response = self.client.put(object_url, film_cinema_attrs)
        self.assertEqual(response.status_code, put_status)

        # DELETE
        response = self.client.delete(object_url)
        self.assertEqual(response.status_code, delete_status)

    def post(self, user, token, post_status):
        """Test post method.

        Args:
            user: user to authenticate
            token: token to authenticate
            post_status: status which asserts
        """
        self.client.force_authenticate(user=user, token=token)
        url = '/rest/film_cinema/'

        film = Film.objects.create(**test_film_attrs)
        address = Address.objects.create(**test_address_attrs)
        cinema = Cinema.objects.create(name='test', address=address)

        film_id = create_hyperlink(film.id, 'film')
        cinema_id = create_hyperlink(cinema.id, 'cinema')

        film_cinema_attrs = {'film': film_id, 'cinema': cinema_id}

        # POST
        response = self.client.post(url, film_cinema_attrs)
        self.assertEqual(response.status_code, post_status)

    def test_manage_user(self):
        """Test manage for user."""
        self.post(self.user, self.user_token, status.HTTP_403_FORBIDDEN)
        self.manage(
            self.user, self.user_token,
            put_status=status.HTTP_403_FORBIDDEN,
            delete_status=status.HTTP_403_FORBIDDEN,
        )

    def test_manage_superuser(self):
        """Test manage for superuser."""
        self.post(self.superuser, self.superuser_token, status.HTTP_201_CREATED)
        self.manage(
            self.superuser, self.superuser_token,
            put_status=status.HTTP_200_OK,
            delete_status=status.HTTP_204_NO_CONTENT,
        )


class TicketTest(WithAuthTest):
    """Class for testing ticket."""

    def get_ticket_filmcinema_attrs(self) -> tuple:
        """Return ticket and filmcinema attrs.

        Returns:
            tuple: film cinema and ticket attrs
        """
        film = Film.objects.create(**test_film_attrs)
        address = Address.objects.create(**test_address_attrs)
        cinema = Cinema.objects.create(name='test', address=address)
        film_cinema = FilmCinema.objects.create(film=film, cinema=cinema)
        current_date = datetime.now(tz=timezone.utc)
        ticket_attrs = {'film_date': current_date, 'place': 'test_place', 'film_cinema': film_cinema}
        return film_cinema, ticket_attrs

    def manage(self, user: User, token: Token, put_status: int, delete_status: int):
        """Test put and delete methods.

        Args:
            user: user to authenticate
            token: token to authenticate
            put_status : status which asserts for put
            delete_status (int): status which asserts for delete
        """
        self.client.force_authenticate(user=user, token=token)
        url = '/rest/ticket/'
        film_cinema, ticket_attrs = self.get_ticket_filmcinema_attrs()
        ticket_id = Ticket.objects.create(**ticket_attrs).id
        ticket_attrs['film_cinema'] = create_hyperlink(film_cinema.id, 'film_cinema')

        self.client.session.save()

        object_url = f'{url}{ticket_id}/'

        # PUT
        response = self.client.put(object_url, ticket_attrs)
        self.assertEqual(response.status_code, put_status)

        # DELETE
        response = self.client.delete(object_url)
        self.assertEqual(response.status_code, delete_status)

    def post(self, user: User, token: Token, post_status: int):
        """Test post method.

        Args:
            user: user to authenticate
            token: token to authenticate
            post_status: status which asserts
        """
        self.client.force_authenticate(user=user, token=token)
        url = '/rest/ticket/'
        film_cinema, ticket_attrs = self.get_ticket_filmcinema_attrs()
        ticket_attrs['film_cinema'] = create_hyperlink(film_cinema.id, 'film_cinema')
        response = self.client.post(url, ticket_attrs)
        self.assertEqual(response.status_code, post_status)

    def test_manage_user(self):
        """Test manage for user."""
        self.post(self.user, self.user_token, status.HTTP_201_CREATED)
        self.manage(
            self.user, self.user_token,
            put_status=status.HTTP_200_OK,
            delete_status=status.HTTP_204_NO_CONTENT,
        )

    def test_manage_superuser(self):
        """Test manage for superuser."""
        self.post(self.superuser, self.superuser_token, status.HTTP_201_CREATED)
        self.manage(
            self.superuser, self.superuser_token,
            put_status=status.HTTP_200_OK,
            delete_status=status.HTTP_204_NO_CONTENT,
        )
