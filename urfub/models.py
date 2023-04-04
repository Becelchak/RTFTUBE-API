from django.db import models
from embed_video.fields import EmbedVideoField

class videos(models.Model):
    id = models.IntegerField(primary_key=True)
    url = EmbedVideoField(null=False)
    video_name = models.CharField(max_length=100, null=False)
    likes = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    def __str__(self):
        return str(self.video_name)

    class Meta:
        ordering = ['-id']