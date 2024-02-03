from django.db import models

class Video(models.Model):
    video_id = models.CharField(max_length=20, unique=True)  
    published_at = models.DateTimeField()  
    title = models.TextField()
    description = models.TextField()
    thumbnail_url = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['published_at']),
        ]
