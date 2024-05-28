from django.test import TestCase, client as test_client
from django.contrib.auth.models import User
from cinephile_server.models import Ticket, FilmCinema, Film, Cinema
from rest_framework import status

class BookTicketTest(TestCase):
    def setUp(self) -> None:
        self.client = test_client.Client()
        self.user = User.objects.create_user(username='user', password='user')
        self.client.force_login(self.user)
        cinema = Cinema.objects.create(name="Test Cinema", address="123 Test Street")
        film = Film.objects.create(name="Test Film", description="A great film.", rating=1)
        film_cinema = FilmCinema.objects.create(cinema=cinema, film=film)
        self.ticket = Ticket.objects.create(time="20:00", place="Seat 1", price=100.00, film_cinema=film_cinema)
        self.book_ticket_url = f'/book_tickets/?ticket_id={self.ticket.id}'

    def test_book_ticket_authenticated(self):
        response = self.client.post(self.book_ticket_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Ticket.objects.filter(id=self.ticket.id).exists())

    def test_book_ticket_not_authenticated(self):
        self.client = test_client.Client()
        response = self.client.post(self.book_ticket_url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_non_post_request(self):
        response = self.client.get(self.book_ticket_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Something went wrong...', response.content.decode())
