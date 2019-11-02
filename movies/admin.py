from django.contrib import admin
from .models import (
    Movie,
    MovieMetadata,
    MovieGenre,
    Genre,
    PlayHistory
)

class MovieGenreInline(admin.StackedInline):
    model = MovieGenre
    extra = 1

class MovieMetadataInline(admin.StackedInline):
    model = MovieMetadata
    extra = 1

class MovieAdmin(admin.ModelAdmin):
    inlines = [
            MovieGenreInline,
            MovieMetadataInline,
    ]


admin.site.register(PlayHistory)
admin.site.register(Genre)
admin.site.register(Movie, MovieAdmin)
