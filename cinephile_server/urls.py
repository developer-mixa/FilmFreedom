"""Module for urls."""


from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from cinephile_server import views

router = DefaultRouter()
router.register(r'cinema', views.CinemaViewSet, 'cinema')
router.register(r'film', views.FilmViewSet, 'film')
router.register(r'film_cinema', views.FilmCinemaViewSet, 'filmcinema')
router.register(r'ticket', views.TicketViewSet, 'ticket')
router.register(r'user', views.UserViewSet, 'user')

urlpatterns = [
    path('rest/', include(router.urls)),
    path('', views.main_page),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', views.profile_page, name='profile'),
    path('accounts/register/', views.register_page, name='register'),
    path('films/', views.films_page),
    path('cinemas/', views.cinemas_page),
    path('films/<uuid:pk>/', views.film_detail_page, name='film'),
    path('cinemas/<uuid:pk>/', views.cinema_detail_page, name='cinema'),
    path('book_tickets/', views.book_ticket, name='book_ticket'),
    path('cancel_ticket/', views.cancel_ticket, name='cancel_ticket'),
    path('tickets/', views.booked_tickets_page, name='tickets'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
