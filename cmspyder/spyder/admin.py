from django.contrib import admin

from models import Domain
from tasks import discover_type


class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain', 'type', 'last_crawl']
    ordering = ['domain']
    actions = ['discover_type']

    def discover_type(self, request, queryset):
        for domain in queryset:
            result = discover_type.delay(domain.id)
        self.message_user(request, 'Task(s) created')
    discover_type.short_description = 'Discover the type of the blog(s)'

admin.site.register(Domain, DomainAdmin)
