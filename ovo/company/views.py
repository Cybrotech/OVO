from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response

from my_user.models import CustomUser

from .forms import *
from .models import UserProfile

def register_company(request):
    if request.user.is_authenticated():
        return redirect(reverse_lazy('add_website'))
    if request.method == "POST":
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = CustomUser(email=form.cleaned_data['email'],
                              first_name=form.cleaned_data['name'],
                              last_name=form.cleaned_data['surname'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            profile = UserProfile(user=user,
                                  mobile=form.cleaned_data['mobile_number'],
                                  role=form.cleaned_data['role'],
                                  registered_for=form.cleaned_data['register_for'])
            profile.save()
            form.instance.user = user
            form.save()
            return redirect(reverse_lazy('login'))
    else:
        form = CompanyRegistrationForm()
    return render_to_response("company/register.html",
                  {'form': form}, context_instance=RequestContext(request))

@login_required
def dummy(request):
    return render(request, "company/dummy.html")

def mail_confirmation(request):
    return render(request, "company/mail_confirm.html")
