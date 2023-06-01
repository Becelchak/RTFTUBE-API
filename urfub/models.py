import django.utils.timezone
from django.conf import settings
from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from embed_video.fields import EmbedVideoField

class videos(models.Model):
    id = models.IntegerField(primary_key=True)
    # stream = models.FileField(
    #     upload_to='video/',
    #     validators=[FileExtensionValidator(['mp4'])]
    # )
    key = models.CharField(max_length=100, null=False, default='Atom')
    url_storage = EmbedVideoField(max_length=500,null=False, default="https://youtu.be/gKVXaMeazAQ")
    title = models.CharField(max_length=100, null=False)
    likes = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    publish_date = models.DateField(default=django.utils.timezone.datetime.today().strftime('%Y-%m-%d'))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='creator',
        on_delete=models.CASCADE)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name='liked_users',
                                   default=None
                                   )
    disliked = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name='disliked_users',
                                   default=None
                                   )

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['-id']