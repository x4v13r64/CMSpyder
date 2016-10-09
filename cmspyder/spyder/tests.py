from django.test import TestCase

from domains.models import *
from spyder.tasks import detect_cms


class DetectCMSTestCase(TestCase):
    def setUp(self):
        com_tld = TLD.objects.create(tld='com')
        google_domain = Domain.objects.create(tld=com_tld,
                                              domain='google')
        google_subdomain = Subdomain.objects.create(domain=google_domain)

    def test_detect_cms(self):
        subdomains = Subdomain.objects.filter()

        assert subdomains

        detect_cms(subdomains[0].id)
