from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('address', nargs=1)

    def handle(self, *args, **options):

