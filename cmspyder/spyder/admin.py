from django.contrib import admin

from models import TLD, Domain, PluginResult, ScanResult, Subdomain
from tasks import detect_cms


class TLDAdmin(admin.ModelAdmin):
    search_fields = ['tld']
admin.site.register(TLD, TLDAdmin)


class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain', 'tld']
    list_filter = ['tld']
    search_fields = ['domain', 'tld']
admin.site.register(Domain, DomainAdmin)


class SubdomainAdmin(admin.ModelAdmin):
    list_display = ['subdomain', 'domain', 'get_domain_tld']
    list_filter = ['domain', 'domain__tld']
    search_fields = ['subdomain']

    def get_domain_tld(self, obj):
        return obj.domain.tld
    get_domain_tld.short_description = 'TLD'
    get_domain_tld.admin_order_field = 'domain__tld'

    actions = ['detect_cms']
    def detect_cms(self, request, queryset):
        for subdomain in queryset:
            detect_cms.delay(subdomain.id)
        self.message_user(request, 'Task(s) created')
    detect_cms.short_description = 'Detect CMS'
admin.site.register(Subdomain, SubdomainAdmin)


class ScanResultAdmin(admin.ModelAdmin):
    list_display = ['subdomain', 'type', 'version']
    list_filter = ['subdomain', 'type']
admin.site.register(ScanResult, ScanResultAdmin)
