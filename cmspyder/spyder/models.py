from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Domain(models.Model):
    domain = models.CharField()
    BLOG_TYPES = (
        ('none', 'Unknonw'),
        ('wordpress', 'WordPress'),
    )
    type = models.CharField(max_length=50, choices=BLOG_TYPES, default='none', null=True)
    last_crawl = models.DateTimeField('Last crawl', blank=True, null=True)
