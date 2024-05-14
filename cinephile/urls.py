from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from cinephile_server.views import UserCreate, CinemaCreate, CinemaUpdateDestroy
from cinephile_server.views import FilmCreate, FilmUpdateDestroy
from cinephile_server.views import TicketCreate, TicketUpdateDestroy
from cinephile_server.views import FilmCinemaCreate, FilmCinemaUpdateDestroy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('accounts/register', UserCreate.as_view()),
    path('rest/cinemas/', CinemaCreate.as_view(), name='cinema-list-create'),
    path('rest/cinemas/<uuid:pk>/', CinemaUpdateDestroy.as_view(), name='cinema-detail'),
    path('rest/films/', FilmCreate.as_view(), name='film-list-create'),
    path('rest/films/<uuid:pk>/', FilmUpdateDestroy.as_view(), name='film-detail'),
    path('rest/tickets/', TicketCreate.as_view(), name='ticket-list-create'),
    path('rest/tickets/<uuid:pk>/', TicketUpdateDestroy.as_view(), name='ticket-detail'),
    path('rest/film_cinemas/', FilmCinemaCreate.as_view(), name='film-cinema-list-create'),
    path('rest/film_cinemas/<uuid:pk>/', FilmCinemaUpdateDestroy.as_view(), name='film-cinema-detail'),
]
