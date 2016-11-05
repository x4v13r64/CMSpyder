from django.contrib import admin

from spyder.models import PluginResult, ScanError, ScanResult


class ScanResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'subdomain', 'type', 'version']
    list_filter = ['type']
    search_fields = ['subdomain__subdomain', 'subdomain__domain__domain']
    readonly_fields = ['subdomain', 'type', 'version']
admin.site.register(ScanResult, ScanResultAdmin)


class ScanErrorAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'subdomain', 'type']
    list_filter = ['type']
    search_fields = ['subdomain__subdomain', 'subdomain__domain__domain']
    readonly_fields = ['subdomain', 'type', 'error']
admin.site.register(ScanError, ScanErrorAdmin)
