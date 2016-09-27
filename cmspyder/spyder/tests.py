from spyder.tasks import detect_cms
from domains.models import *

from django.test import TestCase


class DetectCMSTestCase(TestCase):
    def setUp(self):
        com_tld = TLD.objects.create(tld='com')
        google_domain = Domain.objects.create(tld=com_tld,
                                              domain='google')
        google_subdomain = Subdomain(domain=google_domain)

    def test_detect_cms(self):
        google_subdomain = Subdomain.objects.get(domain='google')
        detect_cms(google_subdomain.id)
