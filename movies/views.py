from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView
from . import models
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# For REST
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .serializers import MovieSerializer, PersonSerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
# For Class Based REST views
from rest_framework import generics

# Create your views here.


class MovieHomeView(ListView):
    model = models.Movie
    template_name = 'movies/home.html'
    context_object_name = 'movies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user.is_authenticated
        context['userDetail'] = self.request.user
        context['title'] = 'Movies: Home'
        return context

    def get_queryset(self):
        return models.Movie.objects.order_by('-release_date')[:5]


class MovieView(DetailView):
    model = models.Movie
    template_name = 'movies/movie.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        persons = models.MoviePerson.objects.filter(film=context['movie'])
        context['persons'] = persons
        context['user'] = self.request.user.is_authenticated
        context['userDetail'] = self.request.user
        context['rating'] = [1, 2, 3, 4, 5]
        return context


class PersonView(DetailView):
    model = models.Person
    template_name = 'movies/person.html'
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movies = models.MoviePerson.objects.filter(person=context['person'])
        context['movies'] = movies
        context['user'] = self.request.user.is_authenticated
        context['userDetail'] = self.request.user
        return context


@login_required
def rate_movie(request, movie_id):
    movie = models.Movie.objects.get(id=movie_id)
    if request.method == 'POST':
        user = models.User.objects.get(id=request.user.id)
        rating = int(str(request.POST['rating']))
        if models.MovieRate.objects.complex_filter(Q(user=user) & Q(film=movie)).count() == 0:
            movie_rate = models.MovieRate()
            movie_rate.film = movie
            movie_rate.user = user
            movie_rate.rate = rating
            movie.rating = (movie.rating * movie.raters + rating)/(movie.raters + 1)
            movie.raters += 1
        else:
            movie_rate = models.MovieRate.objects.get(Q(user=user) & Q(film=movie))
            old_rating = movie_rate.rate
            movie_rate.rate = rating
            movie.rating = (movie.rating * movie.raters - old_rating + rating)/movie.raters
        movie_rate.save()
        movie.save()
    return redirect('movie_detail', pk=movie_id)


class MoviesList(generics.ListCreateAPIView):
    queryset = models.Movie.objects.all()
    serializer_class = MovieSerializer


class MovieDetail(generics.RetrieveAPIView):
    queryset = models.Movie.objects.all()
    serializer_class = MovieSerializer


class PersonsList(generics.ListCreateAPIView):
    queryset = models.Person.objects.all()
    serializer_class = PersonSerializer


class PersonDetail(generics.RetrieveAPIView):
    queryset = models.Person.objects.all()
    serializer_class = PersonSerializer


