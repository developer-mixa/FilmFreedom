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
    path('', include('cinephile_server.urls')),
]
