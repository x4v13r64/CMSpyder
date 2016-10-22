from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError


class TLD(models.Model):
    tld = models.CharField(blank=False,
                           max_length=250,
                           default=None)

    def __unicode__(self):
        return u"{}".format(self.tld)

    class Meta(object):
        verbose_name = 'TLD'
        verbose_name_plural = 'TLDs'
        ordering = ('tld',)


class Domain(models.Model):
    tld = models.ForeignKey(TLD, related_name='domain')
    domain = models.CharField(blank=False,
                              max_length=250,
                              default=None)

    def __unicode__(self):
        return u"{}.{}".format(self.domain, self.tld)

    class Meta(object):
        verbose_name = 'Domain'
        verbose_name_plural = 'Domains'
        unique_together = [('domain', 'tld')]
        ordering = ('domain',)


class Subdomain(models.Model):
    domain = models.ForeignKey(Domain, related_name='subdomain')
    subdomain = models.CharField(max_length=250, blank=True)
    last_scan = models.DateTimeField(auto_now_add=True)
    last_ip = models.GenericIPAddressField(null=True)

    def __unicode__(self):
        if self.subdomain:
            return u"{}.{}".format(self.subdomain, self.domain)
        else:
            return self.domain.__unicode__()

    class Meta(object):
        verbose_name = 'Subdomain'
        verbose_name_plural = 'Subdomains'
        unique_together = [('subdomain', 'domain')]
        ordering = ('subdomain',)
