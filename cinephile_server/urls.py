from django.urls import path
from django.urls import path
from cinephile_server.views import CinemaCreate, CinemaUpdateDestroy
from cinephile_server.views import FilmCreate, FilmUpdateDestroy
from cinephile_server.views import TicketCreate, TicketUpdateDestroy
from cinephile_server.views import FilmCinemaCreate, FilmCinemaUpdateDestroy
from cinephile_server.views import main_page, films_page, cinemas_page, film_detail_page

urlpatterns = [
    path('rest/cinemas/', CinemaCreate.as_view(), name='rest-cinema-list-create'),
    path('rest/cinemas/<uuid:pk>/', CinemaUpdateDestroy.as_view(), name='rest-cinema-detail'),
    path('rest/films/', FilmCreate.as_view(), name='rest-film-list-create'),
    path('rest/films/<uuid:pk>/', FilmUpdateDestroy.as_view(), name='rest-film-detail'),
    path('rest/tickets/', TicketCreate.as_view(), name='rest-ticket-list-create'),
    path('rest/tickets/<uuid:pk>/', TicketUpdateDestroy.as_view(), name='rest-ticket-detail'),
    path('rest/film_cinemas/', FilmCinemaCreate.as_view(), name='rest-film-cinema-list-create'),
    path('rest/film_cinemas/<uuid:pk>/', FilmCinemaUpdateDestroy.as_view(), name='rest-film-cinema-detail'),
    path('', main_page),
    path('films/', films_page),
    path('cinemas/', cinemas_page),
    path('films/<uuid:pk>/', film_detail_page, name='film')
]