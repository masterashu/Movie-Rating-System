from rest_framework import serializers
from movies.models import Movie, Person


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'movie_name', 'release_date', 'rating', 'raters')


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'dob', 'sex')
