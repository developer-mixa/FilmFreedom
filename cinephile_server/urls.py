from django.urls import path, include
from django.contrib.auth import views as auth_views
from cinephile_server.views import CinemaCreate, CinemaUpdateDestroy
from cinephile_server.views import FilmCreate, FilmUpdateDestroy
from cinephile_server.views import TicketCreate, TicketUpdateDestroy
from cinephile_server.views import FilmCinemaCreate, FilmCinemaUpdateDestroy
from cinephile_server import views


urlpatterns = [
    path('rest/cinemas/', CinemaCreate.as_view(), name='rest-cinema-list-create'),
    path('rest/cinemas/<uuid:pk>/', CinemaUpdateDestroy.as_view(), name='rest-cinema-detail'),
    path('rest/films/', FilmCreate.as_view(), name='rest-film-list-create'),
    path('rest/films/<uuid:pk>/', FilmUpdateDestroy.as_view(), name='rest-film-detail'),
    path('rest/tickets/', TicketCreate.as_view(), name='rest-ticket-list-create'),
    path('rest/tickets/<uuid:pk>/', TicketUpdateDestroy.as_view(), name='rest-ticket-detail'),
    path('rest/film_cinemas/', FilmCinemaCreate.as_view(), name='rest-film-cinema-list-create'),
    path('rest/film_cinemas/<uuid:pk>/', FilmCinemaUpdateDestroy.as_view(), name='rest-film-cinema-detail'),
    path('', views.main_page),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', views.profile_page, name='profile'),
    path('accounts/register/', views.register_page, name='register'),
    path('films/', views.films_page),
    path('cinemas/', views.cinemas_page),
    path('films/<uuid:pk>/', views.film_detail_page, name='film'),
    path('cinemas/<uuid:pk>/', views.cinema_detail_page, name='cinema'),
    path('book_tickets/', views.book_ticket, name='book_ticket'),
    path('tickets/', views.booked_tickets_page, name='tickets'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout')
]