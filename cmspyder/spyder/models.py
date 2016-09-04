from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Domain(models.Model):
    domain = models.CharField(max_length=250)
    BLOG_TYPES = (
        (None, 'Unknown'),
        ('wordpress', 'WordPress'),
    )
    type = models.CharField(max_length=50, choices=BLOG_TYPES, default=None, null=True)
    last_crawl = models.DateTimeField('Last crawl', blank=True, null=True)
