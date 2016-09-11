from __future__ import unicode_literals

from django.db import models
from model_utils.models import TimeStampedModel

from domains.models import Domain, Subdomain


# BLOG_TYPES = (
#     ('wordpress', 'WordPress'),
# )


class ScanResult(TimeStampedModel):
    subdomain = models.ForeignKey(Subdomain, related_name='scan')
    type = models.CharField(max_length=250)
    version = models.CharField(max_length=50, blank=True)


class PluginResult(models.Model):
    scan_result = models.ForeignKey(Domain, related_name='plugin_result')
    name = models.CharField(max_length=250)
    version = models.CharField(max_length=50)
