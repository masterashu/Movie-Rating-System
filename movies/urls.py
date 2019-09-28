from django.urls import path
from .views import MovieHomeView, MovieView, PersonView, rate_movie
# from .views import movie_detail, movie_list, person_detail, person_list
from .views import MoviesList, MovieDetail, PersonDetail, PersonsList

urlpatterns = [
    path('', MovieHomeView.as_view(), name='movie_home'),
    path('movie/<int:pk>/', MovieView.as_view(), name='movie_detail'),
    path('person/<int:pk>/', PersonView.as_view(), name='person_detail'),
    path('rate/<int:movie_id>/', rate_movie, name='rate_movie'),
    # path('movie_api/<int:pk>/', movie_detail, name='movie_detail_api'),
    # path('movie_api/', movie_list, name='movie_list_json'),
    # path('person_api/<int:pk>/', person_detail, name='person_detail_api'),
    # path('person_api/', person_list, name='person_detail_api'),
    path('api/movie/<int:pk>/', MovieDetail.as_view(), name='movie_detail_api'),
    path('api/movie/', MoviesList.as_view(), name='movie_list_json'),
    path('api/person/<int:pk>/', PersonDetail.as_view(), name='person_detail_api'),
    path('api/person/', PersonsList.as_view(), name='person_detail_api'),
]
