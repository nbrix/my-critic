from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from .models import Movie, Critic, Review

class MovieListView(ListView):
    model = Movie
    paginate_by = 25
    ordering = ['title']
    context_object_name = 'movie_list'
    template_name = 'movies/movie_list.html'

class MovieDetailView(DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = 'movies/movie_detail.html'

class CriticListView(ListView):
    model = Critic
    paginate_by = 25
    ordering = ['name']
    context_object_name = 'critic_list'
    template_name = 'movies/critic_list.html'

class CriticDetailView(DetailView):
    model = Review
    context_object_name = 'critic'
    template_name = 'movies/critic_detail.html'

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(critic__id=1)
