from __future__ import unicode_literals

from django.db import models
from model_utils.models import TimeStampedModel

from domains.models import Domain, Subdomain


class ScanResult(TimeStampedModel):
    subdomain = models.ForeignKey(Subdomain, related_name='scan')
    type = models.CharField(max_length=250)
    version = models.CharField(max_length=50, blank=True)


class PluginResult(TimeStampedModel):
    scan_result = models.ForeignKey(Domain, related_name='plugin_result')
    name = models.CharField(max_length=250)
    version = models.CharField(max_length=50, blank=True)


class ScanError(TimeStampedModel):
    subdomain = models.ForeignKey(Subdomain, related_name='error')
    type = models.CharField(max_length=250)
    error = models.TextField()
