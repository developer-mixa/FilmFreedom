from django.contrib import admin
from .models import Film, Cinema, FilmCinema, Ticket
from .forms import FilmForm, TicketForm

#inlines

class FilmCinemaInline(admin.TabularInline):
    model = FilmCinema
    extra = 1
    
#admins

@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    model = Cinema
    inlines = (FilmCinemaInline,)

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    model = Film
    form = FilmForm
    inlines = (FilmCinemaInline,)

@admin.register(Ticket)
class Ticket(admin.ModelAdmin):
    model = Ticket
    form = TicketForm

@admin.register(FilmCinema)
class FilmCinemaAdmin(admin.ModelAdmin):
    model = FilmCinema
