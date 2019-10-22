from django.core.management.base import BaseCommand
from movies.models import Genre

movie_genre = {}
movie_genre[28] = "Action"
movie_genre[12] = "Adventure"
movie_genre[16] = "Animation"
movie_genre[35] = "Comedy"
movie_genre[80] = "Crime"
movie_genre[99] = "Documentary"
movie_genre[18] = "Drama"
movie_genre[10751] = "Family"
movie_genre[14] = "Fantasy"
movie_genre[36] = "History"
movie_genre[27] = "Horror"
movie_genre[10402] = "Music"
movie_genre[9648] = "Mystery"
movie_genre[10749] = "Romance"
movie_genre[878] = "Science Fiction"
movie_genre[10770] = "TV Movie"
movie_genre[53] = "Thriller"
movie_genre[10752] = "War"
movie_genre[37] = "Western"

class Command(BaseCommand):
    help = 'Adds a bunch of Genres'
    def handle(self, *args, **options):
        for gid in movie_genre:
            self.stdout.write(f"Adding {gid}, {movie_genre[gid]}")
            g = Genre(genre_id=gid, genre=movie_genre[gid])
            g.save()
