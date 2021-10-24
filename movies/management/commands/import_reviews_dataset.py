from django.core.management.base import BaseCommand
from ...models import Movie, Critic, Review
import csv

class Command(BaseCommand):
    help = 'Import movie reviews dataset from csv'

    def handle(self, *args, **kwargs):
        with open('rotten_tomatoes_critic_reviews.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            first_row = True
            prev_movie_id = None
            i, n = 0, 0
            for row in reader:

                # skip headers
                if first_row:
                    first_row = False
                    continue

                data = {
                    'id': row[0],
                    'name': row[1],
                    'publisher': row[3],
                    'score': row[5],
                    'date': row[6],
                    'review': row[7]
                }

                # clean data to prevent db errors
                if not data['name']:
                    continue
                for key, value in data.items():
                    if not value:
                        data[key] = None

                try:
                    if prev_movie_id != data['id']:
                        movie = Movie.objects.get(rotten_tomato_id=data['id'])
                        prev_movie_id = data['id']
                except Movie.DoesNotExist:
                    continue

                critic, created = Critic.objects.get_or_create(
                    name=data['name'],
                    publisher=data['publisher']
                )

                review = Review.objects.create(
                    review=data['review'],
                    review_score=data['score'],
                    review_date=data['date'],
                    critic=critic,
                    movie=movie
                ) 
                

                critic.save()
                review.save()
                i += 1
                if i > n:
                    print(i)
                    n += 500
