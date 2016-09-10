from django.contrib import admin

from models import TLD, Domain, Subdomain, ScanResult, PluginResult
from tasks import discover_type


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

#     actions = ['discover_type']
#
#     def discover_type(self, request, queryset):
#         for domain in queryset:
#             discover_type.delay(domain.id)
#         self.message_user(request, 'Task(s) created')
#     discover_type.short_description = 'Discover the type of the blog(s)'

admin.site.register(Subdomain, SubdomainAdmin)
