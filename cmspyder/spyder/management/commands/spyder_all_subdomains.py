from django.core.management.base import BaseCommand

from domains.models import Subdomain
from spyder.tasks import detect_cms


class Command(BaseCommand):
    help = 'Spyder all the subdomains in the database'

    def handle(self, *args, **options):

        subdomains = Subdomain.objects.filter()
        for subdomain in subdomains:
            detect_cms.delay(subdomain.id)
