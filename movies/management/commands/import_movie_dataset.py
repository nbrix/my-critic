from django.core.management.base import BaseCommand
from ...models import Movie, Genre, Director, Actor, Writer
import csv

class Command(BaseCommand):
    help = 'Import movie dataset from csv'

    def handle(self, *args, **kwargs):
        with open('rotten_tomatoes_movies.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            first_row = True
            for row in reader:

                # skip headers
                if first_row:
                    first_row = False
                    continue

                data = {
                    'id': row[0],
                    'title': row[1],
                    'plot': row[2],
                    'rating': row[4],
                    'genre': row[5],
                    'directors': row[6],
                    'writers': row[7],
                    'actors': row[8],
                    'release_date': row[9],
                    'runtime': row[11]
                }

                # clean data to prevent db errors
                for key, value in data.items():
                    if not value:
                        data[key] = None

                movie, created = Movie.objects.get_or_create(
                    title=data['title'],
                    plot=data['plot'],
                    rating=data['rating'],
                    release_date=data['release_date'],
                    runtime=data['runtime']
                ) 
                
                if data['id']:
                    movie.rotten_tomato_id = data['id']

                if data['genre']:
                    genres = [x.strip() for x in data['genre'].split(',')]
                    for genre in genres:
                        genre_obj, created = Genre.objects.get_or_create(genre=genre)
                        movie.genres.add(genre_obj)
                        genre_obj.save()

                if data['directors']:
                    directors = [x.strip() for x in data['directors'].split(',')]
                    for director in directors:
                        director_obj, created = Director.objects.get_or_create(name=director)
                        movie.directors.add(director_obj)
                        director_obj.save()

                if data['actors']:
                    actors = [x.strip() for x in data['actors'].split(',')]
                    for actor in actors:
                        actor_obj, created = Actor.objects.get_or_create(name=actor)
                        movie.actors.add(actor_obj)
                        actor_obj.save()

                if data['writers']:
                    writers = [x.strip() for x in data['writers'].split(',')]
                    for writer in writers:
                        writer_obj, created = Writer.objects.get_or_create(name=writer)
                        movie.writers.add(writer_obj)
                        writer_obj.save()

                movie.save()
