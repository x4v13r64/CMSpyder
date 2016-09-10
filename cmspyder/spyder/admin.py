from django.contrib import admin

from models import TLD, Domain, Subdomain, ScanResult, PluginResult
from tasks import discover_type


class TLDAdmin(admin.ModelAdmin):
    model = TLD
admin.site.register(TLD, TLDAdmin)


class DomainAdmin(admin.ModelAdmin):
    model = Domain
    list_display = ['domain', 'tld']
    list_filter = ['tld']
admin.site.register(Domain, DomainAdmin)

class SubdomainAdmin(admin.ModelAdmin):
    model = Domain
    list_display = ['subdomain', 'domain', 'get_domain_tld']
    list_filter = ['domain', 'domain__tld']

    def get_domain_tld(self, obj):
        return obj.domain.tld
    get_domain_tld.short_description = 'TLD'
    get_domain_tld.admin_order_field = 'domain__tld'

#     actions = ['discover_type']
#     ordering = ['domain']
#
#     def discover_type(self, request, queryset):
#         for domain in queryset:
#             discover_type.delay(domain.id)
#         self.message_user(request, 'Task(s) created')
#     discover_type.short_description = 'Discover the type of the blog(s)'
#
admin.site.register(Subdomain, SubdomainAdmin)


# class ScanResultAdmin(admin.ModelAdmin):
#     model = ScanResult
# admin.site.register(ScanResult, ScanResultAdmin)
