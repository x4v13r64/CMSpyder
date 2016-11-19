from django.test import TestCase

from domains.models import Subdomain, Domain, IP
from domains.utils import extract_subdomain, import_subdomain


class UtilsTestCase(TestCase):

    def setUp(self):
        pass

    def test_extract_subdomain(self):

        # test that invalid urls return None
        self.assertIsNone(extract_subdomain('test1'))
        self.assertIsNone(extract_subdomain('http://test1'))
        self.assertIsNone(extract_subdomain('localhost'))

        # test that urls with IPs saves them
        ip_count = IP.objects.count()
        self.assertIsNone(extract_subdomain('http://127.0.0.1'))
        self.assertIsNone(extract_subdomain('http://127.0.0.1/test'))  # different url, same IP
        self.assertIsNone(extract_subdomain('http://192.168.0.1/test'))
        self.assertIsNone(extract_subdomain('http://127.0.0.1.1'))  # invalid
        self.assertEqual(ip_count+2, IP.objects.count())

        # test that valid urls return object
        self.assertIsNotNone(extract_subdomain('test1.com'))
        self.assertIsNotNone(extract_subdomain('test1.com/test'))
        self.assertIsNotNone(extract_subdomain('www.test.test1.com/test'))

    def test_import_subdomain(self):

        # test that invalid urls return None
        self.assertIsNone(import_subdomain('test2'))
        self.assertIsNone(import_subdomain('http://127.0.0.1'))

        # test that valid urls return object
        domain_count = Domain.objects.count()
        subdomain_count = Subdomain.objects.count()
        self.assertIsNotNone(import_subdomain('test2.com'))
        self.assertIsNotNone(import_subdomain('test2.com/test'))  # different url, same subdomain
        # different subdomain, same domain
        self.assertIsNotNone(import_subdomain('www.test.test2.com/test'))
        self.assertEqual(domain_count+1, Domain.objects.count())
        self.assertEqual(subdomain_count+2, Subdomain.objects.count())
