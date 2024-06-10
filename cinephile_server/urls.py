"""Module for urls."""


from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

import cinephile_server.views.pages as page
import cinephile_server.views.queries as query
import cinephile_server.views.viewsets as viewset

router = DefaultRouter()
router.register(r'cinema', viewset.CinemaViewSet, 'cinema')
router.register(r'film', viewset.FilmViewSet, 'film')
router.register(r'film_cinema', viewset.FilmCinemaViewSet, 'filmcinema')
router.register(r'ticket', viewset.TicketViewSet, 'ticket')
router.register(r'address', viewset.AddressViewSet, 'address')
router.register(r'user', viewset.UserViewSet, 'user')

urlpatterns = [
    path('rest/', include(router.urls)),
    path('', page.main_page),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', page.profile_page, name='profile'),
    path('accounts/register/', page.register_page, name='register'),
    path('films/', page.films_page),
    path('cinemas/', page.cinemas_page),
    path('films/<uuid:pk>/', page.film_detail_page, name='film'),
    path('cinemas/<uuid:pk>/', page.cinema_detail_page, name='cinema'),
    path('book_tickets/', query.book_ticket, name='book_ticket'),
    path('cancel_ticket/', query.cancel_ticket, name='cancel_ticket'),
    path('tickets/', page.booked_tickets_page, name='tickets'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
