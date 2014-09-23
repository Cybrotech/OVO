from django.conf.urls import patterns, include, url

from .views import add_website, add_widgets, owner_api, my_widgets, edit_widget

urlpatterns = patterns('',
                       url(r'^add/$', add_website,
                           name="add_website"),
                       url(r'^widget/add/$', add_widgets,
                           name="add_widget"),
                       url(r'^mywidgets/$', my_widgets,
                           name="mywidgets"),
                       url(r'^owner_api/$', owner_api,
                           name="owner_api"),
                       url(r'^widget/edit/(?P<id>[0-9]+)$', edit_widget,
                           name="edit_widget"),
                       )
