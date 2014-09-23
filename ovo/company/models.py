from django.db import models
from django.conf import settings


class Company(models.Model):
    """
    Represent the company details
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name="company")
    name = models.CharField(max_length=100,
                            db_index=True)
    vat = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100,
                            db_index=True)
    number = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100,
                                   db_index=True)
    province = models.CharField(max_length=100,
                                db_index=True)

    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    """
    Represent the user profile details
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile")
    mobile = models.CharField(max_length=20)
    role = models.CharField(max_length=100)
    registered_for = models.CharField(max_length=20)

    def __unicode__(self):
        return self.registered_for + ' : ' + self.user.email