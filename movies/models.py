from django.db import models
from accounts.models import User
# Create your models here.


class Person(models.Model):
    MALE, FEMALE, OTHER = 'M', 'F', 'O'
    SEX_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'), (OTHER, 'Other'))

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    dob = models.DateField(auto_now=False, auto_now_add=False)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default=MALE)

    class Meta:
        ordering = ('first_name', 'last_name',)

    def __str__(self):
        return str(self.first_name + ' ' + self.last_name)


class Movie(models.Model):
    movie_name = models.CharField(max_length=40)
    release_date = models.DateField(
        'Release Date', auto_now=False, auto_now_add=False)
    rating = models.DecimalField(max_digits=3,  decimal_places=2, default=0.0)
    raters = models.IntegerField(default=0)

    class Meta:
        ordering = ('release_date',)

    def refresh_ratings(self):
        rates = MovieRate.objects.filter(film=self)
        self.raters = rates.count()

    def __str__(self):
        return ' '.join([str(self.movie_name), '(' + str(self.release_date.year) + ')'])


class MoviePerson(models.Model):
    ACTOR = 'AC'
    DIRECTOR = 'DR'
    ROLE_CHOICES = ((ACTOR, 'Actor'), (DIRECTOR, 'Director'))
    character_name = models.CharField(max_length=40)
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    film = models.ForeignKey("Movie", on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default=ACTOR)

    def __str__(self):
        text = [str(self.film.movie_name), str(
            self.person.first_name + ' ' + self.person.last_name), str(self.role)]
        return '|'.join(text)


class MovieRate(models.Model):
    film = models.ForeignKey('Movie', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    rate = models.IntegerField()

    def __str__(self):
        return ' '.join([self.film.movie_name, self.user.first_name, str(self.rate)])
