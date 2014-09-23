from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(
        r'^register/$',
        'audience.views.register_audience',
        name="register_audience"
    ),
    url(
        r'^addcontent/$',
        'audience.views.add_content',
        name="add_content"
    ),
    url(
        r'^addcontentaudience/$',
        'audience.views.add_content_audience',
        name="add_content_audience"
    ),
    url(
        r'^ajax-handler/(?P<func_name>\w{1,40})$',
        'audience.ajax_handle.ajax_request',
        name='ajax_handle'
    ),
    url(
        r'^queries/$',
        'audience.views.collection_ajax',
        name='collection_ajax'
    ),
    url(
        r'^country-api/$',
        'audience.views.country_api',
        name='country_api'
    ),
)
