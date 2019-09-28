from django.contrib import admin

# Register your models here.

from .models import Person, MoviePerson, Movie, MovieRate


admin.site.register(Person)
admin.site.register(MoviePerson)
admin.site.register(Movie)
admin.site.register(MovieRate)
