from django.core.management.base import BaseCommand
from movies.tmdbCaller import DataExtractor

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('query', nargs='+')
        parser.add_argument('--year', nargs=1)

    def handle(self, *args, **options):
        db = DataExtractor()
        query = ' '.join(options['query'])
        year = options['year'][0]
        json_data = db.getMetadata(query, year)
        self.stdout.write(str(json_data))
