from django.db import models
from django.core.exceptions import ValidationError
from uuid import uuid4

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True,blank=True, editable=False, default=uuid4)

    class Meta:
        abstract=True

def check_positive(number: int | float):
    if number < 0:
        raise ValidationError(
            'number must be more than 0!',
            params={'number' : number}
            )
    
def check_rating(rating:  float):
    if rating > 5:
        raise ValidationError(
            'rating must be <= 5!',
            params={'number' : rating}
            )

def check_address_len(address: str):
    if len(address) <= 10:
        raise ValidationError(
            'addres cannot be less than 10!',
            params={'address' : address}
        )

class Cinema(UUIDMixin):
    name = models.TextField(max_length=80, null=False, blank=False)
    address = models.TextField(max_length=1024, null=False, validators=[check_address_len])

    films=models.ManyToManyField('Film', through='FilmCinema', verbose_name='Films')

    class Meta:
        db_table='"api_data"."cinema"'

class Film(UUIDMixin):
    name = models.TextField(max_length=80, null=False, blank=False)
    description = models.TextField(max_length=1024, null=False, blank=False)
    rating = models.DecimalField(decimal_places=1,max_digits=2,null=False, validators=[check_positive, check_rating])    

    cinemas = models.ManyToManyField('Cinema', through='FilmCinema', verbose_name='cinemas')

    class Meta:
        db_table='"api_data"."film"'

class FilmCinema(UUIDMixin):
    cinema = models.ForeignKey(Cinema, verbose_name='cinema', on_delete=models.CASCADE)
    film = models.ForeignKey(Film, verbose_name='film', on_delete=models.CASCADE)

    class Meta:
        db_table = '"api_data"."film_to_cinema"',
        unique_together = (('cinema','film'),)

class Ticket(UUIDMixin):
    time = models.TimeField(null=False),
    place = models.TextField(max_length=256, null=False, blank=False)
    price = models.DecimalField(decimal_places=2,max_digits=10,null=False, validators=[check_positive])

    film_cinema = models.OneToOneField(FilmCinema, on_delete=models.CASCADE)