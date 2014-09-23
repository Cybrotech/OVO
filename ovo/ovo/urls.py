from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'common.views.home', name='index'),
                       url(r'^login/$', 'common.views.login',
                           {
                               "template_name" : "common/login.html",
                               "extra_context" : { "next" : reverse_lazy('add_website')},
                           },
                           name="login"),
                       url(r'^logout/$', 'django.contrib.auth.views.logout',
                           {
                               "next_page" : reverse_lazy('index'),
                           },
                           name="logout"),
                           url(
                              r'^terms/$',
                              'common.views.terms',
                              name='terms'
                          ),
                       url(r'^company/', include('company.urls')),
                       url(r'^website/', include('website.urls')),
                       url(r'^audience/', include('audience.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^account/', include('common.auth_urls')),
)

urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))