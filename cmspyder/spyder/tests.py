from django.test import TestCase

from domains.models import *
from spyder.models import *
from spyder.tasks import *


class DetectCMSTestCase(TestCase):
    def setUp(self):

        com_tld = TLD.objects.create(tld='com')
        org_tld = TLD.objects.create(tld='org')

        drupal_domain = Domain.objects.create(tld=com_tld,
                                              domain='drupal')
        drupal_subdomain = Subdomain.objects.create(domain=drupal_domain)

        wordpress_domain = Domain.objects.create(tld=org_tld,
                                              domain='wordpress')
        wordpress_subdomain = Subdomain.objects.create(domain=wordpress_domain)

        invalid_domain = Domain.objects.create(tld=com_tld,
                                               domain='81f344a7686a80b4c5293e8fdc0b0160c82c06a8')
        invalid_subdomain = Subdomain.objects.create(domain=invalid_domain)

    def test_detect_cms(self):

        scan_result_count = ScanResult.objects.count()
        scan_error_count = ScanError.objects.count()

        for s in Subdomain.objects.all():
            detect_cms(s.id)

        self.assertEqual(scan_result_count+2, ScanResult.objects.count())
        self.assertEqual(scan_error_count, ScanError.objects.count())

    def test_discover_domains(self):

        subdomain_count = Subdomain.objects.count()
        ip_count = IP.objects.count()

        discover_domains(Subdomain.objects.order_by('?').first().id,
                         "none")
        discover_domains(Subdomain.objects.order_by('?').first().id,
                         "<html>"
                         "test1.com"
                         "<a href=http://test2.com>"
                         "<a href=192.168.0.1>"
                         "http://192.168.0.2/test"
                         "</html>")

        self.assertEqual(subdomain_count+1, Subdomain.objects.count())
        self.assertEqual(ip_count+1, IP.objects.count())

