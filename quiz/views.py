from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator
from movies.models import Movie, Review, Rating
from django.db.models import Count

class QuizListView(ListView):
    context_object_name = 'quiz_list'
    template_name = 'quiz/rating_quiz.html'
    paginate_by = 6

    def get_queryset(self):
        movies = (Movie
            .objects.
            annotate(n=Count('review'))
            .order_by('-n')
            .filter(release_date__range=["2018-01-01", "2021-01-31"])
            .exclude(poster__isnull=True)
        )[:50]
        return sorted(movies, key=lambda m: m.standard_deviation, reverse=True)[:18]


