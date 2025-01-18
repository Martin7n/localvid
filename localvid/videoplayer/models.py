import os

from django.db import models

# Create your models here.


class Video(models.Model):
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos/')
    filename = models.TextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.video_file:
            self.filename = os.path.basename(self.video_file.name)

        super().save(*args, **kwargs)


class Note(models.Model):
    comment = models.TextField()
    videos = models.ForeignKey(Video, on_delete=models.CASCADE)