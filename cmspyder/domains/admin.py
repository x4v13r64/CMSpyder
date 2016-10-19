from django.contrib import admin

from models import TLD, Domain, Subdomain
from spyder.tasks import detect_cms


class TLDAdmin(admin.ModelAdmin):
    list_display = ['id', 'tld']
    search_fields = ['tld']
    readonly_fields = ['tld']
admin.site.register(TLD, TLDAdmin)


class DomainAdmin(admin.ModelAdmin):
    list_display = ['id', 'domain', 'tld']
    list_filter = ['tld']
    search_fields = ['domain']
    readonly_fields = ['tld', 'domain']
admin.site.register(Domain, DomainAdmin)


class SubdomainAdmin(admin.ModelAdmin):
    list_display = ['id', 'subdomain', 'domain', 'get_domain_tld', 'last_scan', 'last_ip']
    list_filter = ['domain__tld']
    search_fields = ['subdomain', 'domain__domain']
    readonly_fields = ['domain', 'subdomain', 'last_scan', 'last_ip']

    def get_domain_tld(self, obj):
        return obj.domain.tld
    get_domain_tld.short_description = 'TLD'
    get_domain_tld.admin_order_field = 'domain__tld'

    actions = ['detect_cms']
    def detect_cms(self, request, queryset):
        for subdomain in queryset:
            detect_cms.delay(subdomain.id)
            # detect_cms(subdomain.id)
        self.message_user(request, 'Task(s) created')
    detect_cms.short_description = 'Detect CMS'
admin.site.register(Subdomain, SubdomainAdmin)
