from django.contrib import admin
from .models import ApiKey

class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'blacklisted',)
    list_filter = ('blacklisted',)

admin.site.register(ApiKey, ApiKeyAdmin)
