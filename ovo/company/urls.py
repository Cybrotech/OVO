from django.conf.urls import patterns, include, url

from .views import register_company, dummy, mail_confirmation

urlpatterns = patterns('',
                       url(r'^register/$', register_company,
                           name="register_company"),
                       url(r'^mail/confirmation/$', mail_confirmation,
                           name="mail_confirmation_page"),
                       )
