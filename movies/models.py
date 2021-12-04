import uuid
from django.db import models
from django.utils.text import slugify

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
    rating = models.CharField(max_length=16, blank=True)
    poster = models.URLField(max_length=200, null=True, blank=True)
    average_rating = models.DecimalField(max_digits=8, decimal_places=5, null=True, blank=True)
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

