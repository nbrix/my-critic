import uuid
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()

class Genre(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    genre = models.CharField(max_length=64)

    def __str__(self):
        return self.genre

class Director(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Writer(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Actor(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Critic(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=64)
    publisher = models.CharField(max_length=128, null=True, blank=True)
    publishers = models.ManyToManyField(Publisher, null=True)
    slug = models.SlugField(max_length=200, null=True)

    def __str__(self):
        return self.name

    def all_publishers(self):
        pub_list = [obj.name for obj in self.publishers.all()]
        return ' | '.join(pub_list)

    def last_review(self):
        try:
            return self.review_set.all().order_by('-review_date')[0].review_date
        except:
            return 'N/A'

    '''
    def personalized_match(self):
        try:
            return self.topcritics_set.all()[0].match
        except Exception as e:
            return 0
    '''
    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name)
        super().save(*args, **kwargs)

class Movie(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    rotten_tomato_id = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=200, null=True)
    title = models.CharField(max_length=200)
    plot = models.TextField(null=True, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    directors = models.ManyToManyField(Director, blank=True)
    writers = models.ManyToManyField(Writer, blank=True)
    actors = models.ManyToManyField(Actor, blank=True)
    release_date = models.DateField(null=True, blank=True)
    runtime = models.SmallIntegerField(null=True, blank=True)
    mpaa_rating = models.CharField(max_length=16, blank=True)
    poster = models.URLField(max_length=200, null=True, blank=True)
    average_rating = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    standard_deviation = models.DecimalField(max_digits=8, decimal_places=5, null=True, blank=True)

    def __str__(self):
        return self.title

    def all_genres(self):
        genre_list = [obj.genre for obj in self.genres.all()]
        return ' | '.join(genre_list)

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.title)
        super().save(*args, **kwargs)

class Review(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    critic = models.ForeignKey(Critic, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    review = models.TextField(null=True, blank=True)
    review_score = models.CharField(max_length=16, null=True, blank=True)
    normalized_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    review_date = models.DateField(null=True, blank=True)
    sentiment = models.CharField(max_length=8, null=True, blank=True)

class Rating(models.Model):
    score = models.DecimalField(max_digits=3, 
        decimal_places=1, 
        default = 0.0,
        null=True,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )
    personalized_score = models.DecimalField(max_digits=4, 
        decimal_places=1, 
        default = 0.0,
        null=True,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.movie.title

class TopCritics(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    critic = models.ForeignKey(Critic, on_delete=models.CASCADE)
    match = models.DecimalField(max_digits=5, 
        decimal_places=2, 
        default = 0.0,
        null=True,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )

