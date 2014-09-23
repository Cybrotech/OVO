from django.contrib import admin

# Register your models here.
from .models import Category, Website, Section, WidgetFormat, Widget, WidgetFormatChoice

admin.site.register(Category)
admin.site.register(Website)
admin.site.register(Section)
admin.site.register(WidgetFormat)
admin.site.register(WidgetFormatChoice)
admin.site.register(Widget)
