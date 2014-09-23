import datetime

from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

if "django_mailer" in settings.INSTALLED_APPS:
    from django_mailer import send_mail
else:
    from django.core.mail import send_mail

from company.models import Company
from audience.models import Video
from .email_messages import *

class Category(models.Model):
    category_name = models.CharField(unique=True, max_length=100)
    is_enabled = models.BooleanField(default=True)
    created_date = models.DateField(default=datetime.date.today)

    def __unicode__(self):
        return self.category_name

    class Meta:
        verbose_name = "Vertical Category"
        verbose_name_plural = "Vertical Categories"

class Website(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="websites", null=True, default=None)
    url = models.URLField(unique=True)
    site_name = models.CharField(max_length=100)
    vertical_category = models.ForeignKey(Category, related_name="websites")
    unique_users_per_day = models.BigIntegerField()
    page_views_per_day = models.BigIntegerField()
    unique_users_per_month = models.BigIntegerField()
    page_views_per_month = models.BigIntegerField()

    def __unicode__(self):
        return str(self.site_name)

class Section(models.Model):
    website = models.ForeignKey(Website, related_name="sections")
    url = models.URLField(unique=True)
    section_name = models.CharField(max_length=100)
    allowed_clips = models.ManyToManyField(Video, null=True, blank=True)

    def __unicode__(self):
        return str(self.section_name)


class WidgetFormat(models.Model):
    name = models.CharField(max_length=100)
    is_enabled = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class WidgetFormatChoice(models.Model):
    size = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="widget_format_choice")
    widget_format = models.ForeignKey(WidgetFormat, related_name="widget_format_choice")

    def __unicode__(self):
        return self.widget_format.name + ' ' + self.size + ' : ' + self.user.email


class Widget(models.Model):
    widget_format = models.ForeignKey(WidgetFormat, related_name="widget")
    clips = models.ManyToManyField(Video, related_name="widget", null=True, blank=True)
    sites = models.ManyToManyField(Website, related_name="widget", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="widget", null=True, default=None)

    def __unicode__(self):
        return self.widget_format.name + ' ' + str(self.id)


def send_email_to_content_owners(sender, **kwargs):
    instance = kwargs['instance']
    website_url = instance.url
    from_address = settings.DEFAULT_EMAIL_FROM_ADDRESS
    website_name = settings.WEBSITE_NAME
    try:
        subject = website_registration_email["subject"]
        body = website_registration_email["body"] % (website_url, website_name)
        email_addresses = Company.objects.filter(user__profile__registered_for="website_owner").values_list('user__email')
        if not email_addresses:
            return
        recipients = [x[0] for x in Company.objects.filter(user__profile__registered_for="website_owner").values_list('user__email')]
        for recipient in recipients:
            send_mail(subject, body, from_address, [recipient])
    except:
        return

post_save.connect(send_email_to_content_owners, sender=Website, weak=False)
