from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.utils.cache import patch_cache_control

from django.contrib.auth.views import login as auth_login
from website.static_class import MyClass, MyNewClass


def login(request, *args, **kwargs):
    if request.user.is_authenticated():
        return redirect(reverse_lazy('add_website'))
    else:
        my_class = MyClass()
        my_new_class = MyNewClass()
        my_class.clear()
        my_new_class.clear()
        if request.GET.get('next') is not None:
            kwargs['extra_context']['next'] = request.GET.get('next')
        response = auth_login(request, *args, **kwargs)
        patch_cache_control(response,
                            max_age=0,
                            private=True,
                            no_cache=True,
                            no_store=True,
                            must_revalidate=True)
        return response

def home(request):
    return render(request, "index.html")

def terms(request):
    parameters = {}
    if not request.user.is_superuser:
        if request.user.profile.registered_for == "website_owner":
            parameters['ext'] = 'content'
            parameters['section'] = 'content'
        else:
            parameters['ext'] = 'audience'
            parameters['section'] = 'audience'
    else:
        parameters['ext'] = 'audience'
        parameters['section'] = 'audience'
    parameters['page'] = 'terms'
    return render(request, "termsaudience.html",parameters)