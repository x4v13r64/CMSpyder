from django.contrib import admin

from models import PluginResult, ScanResult




class ScanResultAdmin(admin.ModelAdmin):
    list_display = ['subdomain', 'created', 'type', 'version']
    list_filter = ['subdomain', 'type']
admin.site.register(ScanResult, ScanResultAdmin)
