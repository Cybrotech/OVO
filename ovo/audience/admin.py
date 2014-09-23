from django.contrib import admin
from .models import Collection, Video, Topic, Country
# Register your models here.

admin.site.register(Collection)
admin.site.register(Video)
admin.site.register(Topic)
admin.site.register(Country)
