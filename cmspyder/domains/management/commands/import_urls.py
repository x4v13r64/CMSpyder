from django.core.management.base import BaseCommand

from domains.utils import import_subdomain


class Command(BaseCommand):
    help = 'Import URLs from file to database'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('path_to_file', nargs='+', type=str)

    def handle(self, *args, **options):

        if options['path_to_file']:
            with open(options['path_to_file'][0]) as urls:
                for url in urls:
                    import_subdomain(url)
