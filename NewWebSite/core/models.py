from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='events/', null=True, blank=True)

    def __str__(self):
        return self.title


class SessionPhoto(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='sessions/')
    taken_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title or f'SessionPhoto {self.pk}'
