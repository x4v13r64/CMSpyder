from django.contrib import admin

from models import PluginResult, ScanResult, ScanError


class ScanResultAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_display = ['subdomain', 'created', 'type', 'version']
    list_filter = ['subdomain__subdomain', 'type']
admin.site.register(ScanResult, ScanResultAdmin)


class ScanErrorAdmin(admin.ModelAdmin):
    list_display = ['subdomain', 'created']
    list_filter = ['subdomain__subdomain']
admin.site.register(ScanError, ScanErrorAdmin)
