from django.core.management.base import BaseCommand
from ...models import Movie, Review, Critic
from django.db.models import Avg
from django.db.models.aggregates import StdDev

class Command(BaseCommand):
    help = 'get movie rating averages'

    def handle(self, *args, **kwargs):
        movies = Movie.objects.all()

        i = 0
        total = len(movies)
        for movie in movies:
            i += 1
            print(i, '/', total)

            reviews = movie.review_set
            avg = list(reviews.aggregate(Avg('normalized_score')).values())[0]
            std = list(reviews.aggregate(StdDev('normalized_score')).values())[0]

            movie.average_rating = avg
            movie.standard_deviation = std
            movie.save()
                
#m = Movie.objects.annotate(n=Count('review')).order_by('-n')[:100]
#objs = sorted(m, key=lambda m: m.standard_deviation, reverse=True)
