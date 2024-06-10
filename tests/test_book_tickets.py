"""Module for test booking tickets."""


from datetime import datetime, timezone

from tests.data import test_address_attrs
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import client as test_client
from rest_framework import status

from cinephile_server.models import Address, Cinema, Film, FilmCinema, Ticket


class BookTicketTest(TestCase):
    """Test for booking ticket."""

    def setUp(self) -> None:
        """Set up things for tests."""
        self.client = test_client.Client()
        self.user = User.objects.create_user(username='user', password='user')
        self.client.force_login(self.user)
        address = Address.objects.create(**test_address_attrs)
        cinema = Cinema.objects.create(name='Test Cinema', address=address)
        film = Film.objects.create(name='Test Film', description='A great film.', rating=1)
        film_cinema = FilmCinema.objects.create(cinema=cinema, film=film)
        film_date = datetime.now(tz=timezone.utc)
        self.ticket = Ticket.objects.create(film_date=film_date, place='Seat 1', film_cinema=film_cinema)
        ticket_id = self.ticket.id
        self.book_ticket_url = f'/book_tickets/?ticket_id={ticket_id}'

    def test_book_ticket_authenticated(self):
        """Test authenticated user books ticket."""
        response = self.client.post(self.book_ticket_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Ticket.objects.filter(id=self.ticket.id).exists())

    def test_book_ticket_not_authenticated(self):
        """Test non authenticated user books ticket."""
        self.client = test_client.Client()
        response = self.client.post(self.book_ticket_url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_non_post_request(self):
        """Test we send non post request."""
        response = self.client.get(self.book_ticket_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Something went wrong...', response.content.decode())
