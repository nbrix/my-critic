from django.core.management.base import BaseCommand
from ...models import Movie, Review
import csv

class Command(BaseCommand):
    help = 'Normalize scoring system to common metric'

    def handle(self, *args, **kwargs):
        letter_grades = {
            "F": 50,
            "D": 65,
            "C": 75,
            "B": 85,
            "A": 95
        }

        def is_letter(score):
            letters = ['A', 'B', 'C', 'D', 'F']
            return any(x in score for x in letters)

        def is_fraction(score):
            return '/' in score

        reviews = Review.objects.all()

        i, total = 0, len(reviews)
        for review in reviews:
            i += 1
            if i < 388000:
                continue
            if i % 1000 == 0:
                print(i, '/', total)
            if review.review_score:
                if is_letter(review.review_score):
                    score = letter_grades[review.review_score[0]]
                    if '-' in review.review_score:
                        score -= 4
                    elif '+' in review.review_score:
                        score += 4
                    review.normalized_score = score
                    
                elif is_fraction(review.review_score):     
                    num, denom = review.review_score.split('/')
                    if denom == '0':
                        denom = '10'
                    review.normalized_score = float(num) / float(denom) * 100
                else:
                    review.review_score = None
                review.save()
        
                
