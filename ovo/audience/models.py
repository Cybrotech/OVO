from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


class Topic(models.Model):
    """
    Represents the topics for collections
    """
    topic = models.CharField(max_length=50)

    def __unicode__(self):
        return str(self.topic)


class Collection(models.Model):
    """
    Represents the Collection details
    """
    name = models.CharField(max_length=50, db_index=True)
    topic = models.ForeignKey(Topic, null=True, blank=True)
    user = models.ForeignKey(
        get_user_model(),
        related_name='collection'
    )

    def __unicode__(self):
        return str(self.name)


class Country(models.Model):
    """ Represents the country """
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Video(models.Model):
    """
    Represents the Video details
    """
    video_file = models.FileField(upload_to=settings.MEDIA_ROOT, max_length=250, null=True, blank=True)
    video_url = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    collection = models.ForeignKey(Collection, null=True, blank=True)
    thumbnail = models.ImageField(upload_to=settings.MEDIA_ROOT+'/thumbnails', max_length=250, null=True, blank=True)
    blacklisted_country = models.ManyToManyField(Country, null=True, blank=True)

    def __unicode__(self):
        return str(self.title)
