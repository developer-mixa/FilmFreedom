from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Cinema, Film, Ticket, FilmCinema
from rest_framework.serializers import HyperlinkedModelSerializer


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

class CinemaSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Cinema
        fields = '__all__'

class FilmSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Film
        fields = "__all__"

class TicketSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"

class FilmCinemaSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = FilmCinema
        fields = "__all__"