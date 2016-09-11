from django.contrib import admin

from models import PluginResult, ScanResult, ScanError


class ScanResultAdmin(admin.ModelAdmin):
    list_display = ['subdomain', 'created', 'type', 'version']
    list_filter = ['type']
    search_fields = ['subdomain__subdomain']
admin.site.register(ScanResult, ScanResultAdmin)


class ScanErrorAdmin(admin.ModelAdmin):
    list_display = ['created', 'subdomain']
    search_fields = ['subdomain__subdomain']
admin.site.register(ScanError, ScanErrorAdmin)
