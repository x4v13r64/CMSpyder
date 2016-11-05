from __future__ import unicode_literals

from django.db import models


class TLD(models.Model):
    tld = models.CharField(blank=False,
                           max_length=250,
                           default=None,
                           unique=True)

    def __str__(self):
        return u"{}".format(self.tld)

    class Meta(object):
        verbose_name = 'TLD'
        verbose_name_plural = 'TLDs'
        ordering = ('tld',)

    # TLD should never be an empty string
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.tld == '':
            raise ValidationError('TLD cannot be an empty string.')


class Domain(models.Model):
    tld = models.ForeignKey(TLD, related_name='domain')
    domain = models.CharField(blank=False,
                              max_length=250,
                              default=None)

    def __str__(self):
        return u"{}.{}".format(self.domain, self.tld)

    class Meta(object):
        verbose_name = 'Domain'
        verbose_name_plural = 'Domains'
        unique_together = [('domain', 'tld')]
        ordering = ('domain',)

    # domain should never be an empty string
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.tld == '':
            raise ValidationError('domain cannot be an empty string.')


class Subdomain(models.Model):
    domain = models.ForeignKey(Domain, related_name='subdomain')
    subdomain = models.CharField(max_length=250, blank=True)
    last_scan = models.DateTimeField(auto_now_add=True)
    last_ip = models.GenericIPAddressField(null=True)
    # so that when a subdomain points to another subdomain, we can keep track of the source of
    # the link
    discovered_by = models.ForeignKey('self', null=True, related_name='discovered')

    def __str__(self):
        if self.subdomain:
            return u"{}.{}".format(self.subdomain, self.domain)
        else:
            return self.domain.__str__()

    class Meta(object):
        verbose_name = 'Subdomain'
        verbose_name_plural = 'Subdomains'
        unique_together = [('subdomain', 'domain')]
        ordering = ('subdomain',)


class IP(models.Model):
    ip = models.GenericIPAddressField(null=False)

    def __str__(self):
        return u"{}".format(self.ip)

    class Meta(object):
        verbose_name = 'IP address'
        verbose_name_plural = 'IP addresses'
