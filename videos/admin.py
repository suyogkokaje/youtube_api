from django.contrib import admin

from .models import Video

class VideoAdmin(admin.ModelAdmin):
    ordering = ('-published_at',)
    list_display = ('video_id','title','published_at')

admin.site.register(Video,VideoAdmin)
