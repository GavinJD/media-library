from django.core.management.base import BaseCommand
from movies.models import Genre

tv_genre = {}
tv_genre[10759] = "Action & Adventure"
tv_genre[16] = "Animation"
tv_genre[35] = "Comedy"
tv_genre[80] = "Crime"
tv_genre[99] = "Documentary"
tv_genre[18] = "Drama"
tv_genre[10751] = "Family"
tv_genre[10762] = "Kids"
tv_genre[9648] = "Mystery"
tv_genre[10763] = "News"
tv_genre[10764] = "Reality"
tv_genre[10765] = "Sci-Fi & Fantasy"
tv_genre[10766] = "Soap"
tv_genre[10767] = "Talk"
tv_genre[10768] = "War & Politics"
tv_genre[37] = "Western"

class Command(BaseCommand):
    help = 'Adds a bunch of Genres'
    def handle(self, *args, **options):
        for gid in tv_genre:
            self.stdout.write(f"Adding {gid}, {tv_genre[gid]}")
            g = Genre(genre_id=gid, genre=tv_genre[gid])
            g.save()
