from django.db import models


class Link(models.Model):
    url = models.URLField(max_length=200)
    paused = models.BooleanField(default=False)

    def __str__(self):
        return self.url


class Interval(models.Model):
    """
    Interval for checking Url.
    Singleton.
    """
    value = models.PositiveSmallIntegerField(default=4)

    def save(self, *args, **kwargs):
        self.id = 1
        super(Interval, self).save(*args, **kwargs)
