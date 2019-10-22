from django.contrib import admin
from .models import(
    TVShow,
    TVSeason,
    TVEpisode,
    TVMetadata,
    Genre,
    TVGenre
)


class TVEpisodeInline(admin.StackedInline):
    model = TVEpisode
    extra = 1


class TVSeasonAdmin(admin.ModelAdmin):
    inlines = [TVEpisodeInline, ]


class TVSeasonInline(admin.StackedInline):
    model = TVSeason
    extra = 1


class TVGenreInline(admin.StackedInline):
    model = TVGenre
    extra = 2


class TVMetadataInline(admin.StackedInline):
    model = TVMetadata
    extra = 1


class TVShowAdmin(admin.ModelAdmin):
    inlines = [TVGenreInline, TVMetadataInline, TVSeasonInline]


admin.site.register(TVSeason, TVSeasonAdmin)
admin.site.register(TVShow, TVShowAdmin)
admin.site.register(Genre)
