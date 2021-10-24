from django.contrib import admin
from django import forms
from .models import (
    Movie,
    Actor,
    Director,
    Genre,
    Writer,
    Critic,
    Review
)

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date')
    search_fields = ('title', )
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        object_id = request.resolver_match.kwargs['object_id']

        if db_field.name == 'genres':
            kwargs['queryset'] = Genre.objects.filter(movie__id=object_id)
        if db_field.name == 'actors':
            kwargs['queryset'] = Actor.objects.filter(movie__id=object_id)
        if db_field.name == 'directors':
            kwargs['queryset'] = Director.objects.filter(movie__id=object_id)
        if db_field.name == 'writers':
            kwargs['queryset'] = Writer.objects.filter(movie__id=object_id)

        return super(MovieAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre',)
    search_fields = ('genre', )

class ActorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', )

class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', )

class WriterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', )

class ReviewInline(admin.TabularInline):
    model = Review
    

class CriticAdmin(admin.ModelAdmin):
    list_display = ('name', 'publisher',)
    search_fields = ('name', 'publisher',)
    inlines = [
        ReviewInline,
    ]


admin.site.register(Movie, MovieAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Writer, WriterAdmin)
admin.site.register(Critic, CriticAdmin)

