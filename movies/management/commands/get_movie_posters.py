from django.core.management.base import BaseCommand
from ...models import Movie
import csv

class Command(BaseCommand):
    help = 'Import movie reviews dataset from csv'

    def handle(self, *args, **kwargs):
        with open('MovieGenre.csv', 'r', encoding='ISO-8859-1') as f:
            reader = csv.reader(f)

            i = 0
            first_row = True
            for row in reader:

                # skip headers
                if first_row:
                    first_row = False
                    continue

                data = {
                    'title': row[2][:-7],
                    'poster': row[5],
                }

                Movie.objects.filter(title=data['title']).update(poster=data['poster'])


                print(i)
                i += 1
                
