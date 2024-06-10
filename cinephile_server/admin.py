"""Module for admin settings."""


from django.contrib import admin

from .forms import FilmForm, TicketForm
from .models import Cinema, Film, FilmCinema, Ticket, Address

# inlines


class FilmCinemaInline(admin.TabularInline):
    """Inline for FilmCinema model."""

    model = FilmCinema
    extra = 1

# admins


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    """Admin for Cinema model."""

    model = Cinema
    inlines = (FilmCinemaInline,)


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    """Admin for Film model."""

    model = Film
    form = FilmForm
    inlines = (FilmCinemaInline,)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Admin for Ticket model."""

    model = Ticket
    form = TicketForm


@admin.register(FilmCinema)
class FilmCinemaAdmin(admin.ModelAdmin):
    """Admin for FilmCinema model."""

    model = FilmCinema

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Admin for Address model."""

    model = Address