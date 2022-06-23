from django.urls import path
from .views import MovieListView, MovieDetailView, RateMovieView

urlpatterns = [
    path('', MovieListView.as_view(), name='movie_list'),
    path('rate-movie/', RateMovieView.as_view(), name='rate_movie'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie_detail'),
]