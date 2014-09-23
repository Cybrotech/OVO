from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.forms.formsets import INITIAL_FORM_COUNT
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.http import HttpResponse
import json
from django.db.models import Count
from django.db import IntegrityError
from django.template import RequestContext
from django.shortcuts import render_to_response

from .forms import AddWebsiteForm, AddSectionFormSet
from .models import Section, Website, WidgetFormat, Category, Widget
from audience.models import Video, Collection
from .static_class import MyClass


@login_required
def add_website(request):
    if not request.user.is_superuser:
        if request.user.profile.registered_for == "content_owner":
            return redirect(reverse_lazy('add_content'))
        elif request.user.profile.registered_for == 'website_owner':
            pass
    parameters = {}
    parameters['ext'] = 'content'
    parameters['section'] = 'content'
    all_categories = Category.objects.filter(is_enabled=True)
    parameters['all_categories'] = all_categories
    parameters['js_categories'] = ','.join([str(i.category_name) for i in all_categories])
    static_obj = MyClass()
    
    if request.method == "POST":
        if request.session.get('post_req_count') is not None:
            request.session['post_req_count'] = request.session['post_req_count'] + 1
            if int(request.session['post_req_count'] == 1):
                del static_obj.added_websites[:]

        myDict = dict(request.POST.iterlists())
        site_url = request.POST.get('url-1')
        site_name = request.POST.get('sitename-1')
        usersxday = request.POST.get('usersxday-1')
        vcat = request.POST.get('vcat-1')
        viewxday = request.POST.get('viewxday-1')
        usersxmonth = request.POST.get('usersxmonth-1')
        viewxmonth = request.POST.get('viewxmonth-1')
        
        category_obj = Category.objects.get(category_name=vcat, is_enabled=True)        
        try:
            website_obj = Website.objects.create(
                user=request.user,
                url=site_url,
                site_name=site_name,
                vertical_category=category_obj,
                unique_users_per_day=usersxday,
                page_views_per_day=viewxday,
                unique_users_per_month=usersxmonth,
                page_views_per_month=viewxmonth
            )
        except IntegrityError as e:
            # parameters['message'] = e.__cause__
            parameters['message'] = "Website URL already registered. Use a new one !".upper()
            # return render(request, 'website/add.html', parameters)
            return render_to_response('website/add.html', parameters, context_instance=RequestContext(request))

        section_list = [k for k, v in myDict.iteritems() if k.find('sectionname') != -1]
        section_obj_list = []
        for each_section in section_list:
            section_url = myDict['url-1-sectionurl-' + each_section[-1:]][0]
            section_name = myDict[each_section][0]
            if section_url == "" and section_name == "":
                continue
            section_obj = Section.objects.create(
                website=website_obj,
                url=section_url,
                section_name=section_name
            )
            section_obj_list.append(section_obj)
        website_detail = {'website': website_obj, 'sections': section_obj_list}
        
        static_obj.added_websites.append(website_detail)
        if request.POST.get('redirect_field') == 'redirect':
            static_obj.clear()
            return redirect(reverse_lazy('add_widget'))
        else:
            parameters['added_websites'] = static_obj.added_websites
            return render_to_response('website/add.html', parameters, context_instance=RequestContext(request))
    else:
        static_obj.clear()
        request.session['post_req_count'] = 0
        parameters['added_websites'] = static_obj.added_websites
        return render_to_response('website/add.html', parameters, context_instance=RequestContext(request))

    # if request.method == "POST":
    #     myDict = dict(request.POST.iterlists())
    #     viewxday_list = [k for k, v in myDict.iteritems() if k.startswith('viewxday-')]
    #     for each in viewxday_list:
    #         site_url = myDict['url-' + each[-1:]][0]
    #         site_name = myDict['sitename-' + each[-1:]][0]
    #         usersxday = myDict['usersxday-' + each[-1:]][0]
    #         vcat = myDict['vcat-' + each[-1:]][0]
    #         viewxday = myDict[each][0]
    #         usersxmonth = myDict['usersxmonth-' + each[-1:]][0]
    #         viewxmonth = myDict['viewxmonth-' + each[-1:]][0]

    #         category_obj = Category.objects.get(category_name=vcat, is_enabled=True)
    #         website_obj = Website.objects.create(
    #             user=request.user,
    #             url=site_url,
    #             site_name=site_name,
    #             vertical_category=category_obj,
    #             unique_users_per_day=usersxday,
    #             page_views_per_day=viewxday,
    #             unique_users_per_month=usersxmonth,
    #             page_views_per_month=viewxmonth
    #         )

    #         section_list = [k for k, v in myDict.iteritems() if k.startswith('url-'+ each[-1:] +'-sectionname')]
    #         for each_section in section_list:
    #             section_url = myDict['url-'+ each[-1:] +'-sectionurl-' + each_section[-1:]][0]
    #             section_name = myDict[each_section][0]

    #             section_obj = Section.objects.create(
    #                 website=website_obj,
    #                 url=section_url,
    #                 section_name=section_name
    #             )
    #     return redirect(reverse_lazy('add_widget'))
    # return render(request, 'website/add.html', parameters)


def dummy(request):
    return render(request,
                  "website/dummy.html")

@login_required
def add_widgets(request):
    if not request.user.is_superuser:
        if request.user.profile.registered_for == "content_owner":
            return redirect(reverse_lazy('add_content'))
        elif request.user.profile.registered_for == 'website_owner':
            pass
    context = {}
    context['page'] = 'widgets'
    # content_owner = {}
    context['collection_data'], context['video_count'] = return_owner_details()
    context["websites"] = Website.objects.filter(user=request.user)
    # context['collection_data'] = new_return_owner_details(context['websites'])
    context["content_owners"] = get_user_model().objects.filter(profile__registered_for="content_owner")
    context["widget_formats"] = WidgetFormat.objects.all()
    if request.method == 'POST':
        myDict = dict(request.POST.iterlists())
        widget_format_id = int(myDict['widget_format'][0])
        widget_format_obj = WidgetFormat.objects.get(id=widget_format_id)
        widget_obj = Widget.objects.create(widget_format=widget_format_obj, user=request.user)

        section_list = [k for k, v in myDict.iteritems() if k.find('section') != -1]
        raw_website_id_list = []
        for each_section in section_list:
            sec_id = int(myDict[each_section][0])
            section_obj = Section.objects.get(id=sec_id)
            raw_website_id_list.append(section_obj.website.id)

        final_website_id_list = list(set(raw_website_id_list))
        for each_site in final_website_id_list:
            widget_obj.sites.add(Website.objects.get(id=each_site))


        video_list = [k for k, v in myDict.iteritems() if k.find('video') != -1]
        for each_video in video_list:
            video_id = int(myDict[each_video][0])
            video_obj = Video.objects.get(id=video_id)
            widget_obj.clips.add(video_obj)
        return redirect(reverse_lazy('mywidgets'))
    return render_to_response("website/add_widgets.html", context, context_instance=RequestContext(request))

@login_required
def my_widgets(request):
    if not request.user.is_superuser:
        if request.user.profile.registered_for == "content_owner":
            return redirect(reverse_lazy('add_content'))
        elif request.user.profile.registered_for == 'website_owner':
            pass    
    parameters = {}
    parameters['ext'] = 'content'
    parameters['section'] = 'content'
    parameters['page'] = 'widgets'

    grouped_widgets = Widget.objects.filter(user__id=request.user.id).values('widget_format').annotate(widget_count=Count('widget_format'))
    all_widgets = []
    for each_type in grouped_widgets:
        widget_format = WidgetFormat.objects.get(id=int(each_type['widget_format']))
        type_widgets = Widget.objects.filter(user__id=request.user.id, widget_format=widget_format)
        widget_details = {
            'widget_type': widget_format,
            'widget_count': int(each_type['widget_count']),
            'widgets': type_widgets
        }
        all_widgets.append(widget_details)
    parameters['all_widgets'] = all_widgets
    return render_to_response("website/widgets.html", parameters, context_instance=RequestContext(request))

@login_required
def edit_widget(request, id):
    if not request.user.is_superuser:
        if request.user.profile.registered_for == "content_owner":
            return redirect(reverse_lazy('add_content'))
        elif request.user.profile.registered_for == 'website_owner':
            pass
    context = {}
    widget_obj = Widget.objects.get(id=id)
    if widget_obj.user != request.user:
        return redirect(reverse_lazy('mywidgets'))
    allowed_clips = [ i for i in widget_obj.clips.all()]
    context['allowed_sites'] = [ int(i.id) for i in widget_obj.sites.all()]

    context['allowed_collections'] = [int(i.collection.id) for i in allowed_clips]
    context['allowed_clips'] = [int(i.id) for i in allowed_clips]

    context['collection_data'], context['video_count'] = return_owner_details()
    context["websites"] = Website.objects.filter(user=request.user)
    # context['collection_data'] = new_return_owner_details(context['websites'])
    context["content_owners"] = get_user_model().objects.filter(profile__registered_for="content_owner")
    context["widget_formats"] = WidgetFormat.objects.all()
    context['mywidget'] = widget_obj
    if request.method == 'POST':
        myDict = dict(request.POST.iterlists())
        widget_format_id = int(myDict['widget_format'][0])
        widget_format_obj = WidgetFormat.objects.get(id=widget_format_id)
        widget_obj.widget_format = widget_format_obj
        widget_obj.save()

        section_list = [k for k, v in myDict.iteritems() if k.find('section') != -1]
        raw_website_id_list = []
        for each_section in section_list:
            sec_id = int(myDict[each_section][0])
            section_obj = Section.objects.get(id=sec_id)
            raw_website_id_list.append(section_obj.website.id)

        final_website_id_list = list(set(raw_website_id_list))
        widget_obj.clips.clear()
        widget_obj.sites.clear()
        for each_site in final_website_id_list:
            widget_obj.sites.add(Website.objects.get(id=each_site))


        video_list = [k for k, v in myDict.iteritems() if k.find('video') != -1]
        for each_video in video_list:
            video_id = int(myDict[each_video][0])
            video_obj = Video.objects.get(id=video_id)
            widget_obj.clips.add(video_obj)

        return redirect(reverse_lazy('mywidgets'))
    return render_to_response("website/edit_widget.html", context, context_instance=RequestContext(request))

@login_required
def owner_api(request):
    data, video_count = return_owner_details()
    return HttpResponse(json.dumps(data))


def return_owner_details():
    data = []
    content_owner = {}
    video_count = 0
    for content_owner in get_user_model().objects.filter(profile__registered_for="content_owner"):
        owner_video_count = 0
        content_owner_data = {}
        content_owner_data['owner'] = {'name' : content_owner.company.name, 'id': content_owner.company.id }
        collections = []
        for collection in content_owner.collection.all():
            collection_data = {}
            collection_data['collection'] = {'name' : collection.name, 'id': collection.id }

            video_data = []
            for video in collection.video_set.all():
                video_dict = {}
                if video.video_url is None or video.video_url == '':
                    if video.video_file is not None:
                        video_dict['video_url'] = video.video_file.url
                    else:
                        video_dict['video_url'] = ''
                else:
                    video_dict['video_url'] = video.video_url
                video_dict['title'] = video.title
                video_dict['id'] = video.id
                video_dict['description'] = video.description
                if video.thumbnail != None:
                    video_dict['thumbnail'] = video.thumbnail.name
                else:
                    video_dict['thumbnail'] = '/static/company/images/videothumb.jpg'
                video_data.append(video_dict)
                video_count = video_count + 1
                owner_video_count = owner_video_count + 1
            collection_data['videos'] = video_data
            collections.append(collection_data)
        

        content_owner_data['collections'] = collections
        content_owner_data['owner_video_count'] = owner_video_count

        data.append(content_owner_data)
    return data, video_count


def new_return_owner_details(websites):
    data = []
    raw_allowed_clips = []
    raw_allowed_collections = []
    for each_website in websites:

        allowed_clips_ids = [i.id for i in each_website.section.model.allowed_clips.through]
        allowed_clips = [i for i in each_website.section_set.allowed_clips.all()]
        allowed_collections_ids = [i.collection.id for i in allowed_clips]
        raw_allowed_clips.extend(allowed_clips)
        raw_allowed_collections.extend()

    final_allowed_clips = list(set(raw_allowed_clips))
    final_allowed_collections = list(set(raw_allowed_collections))

    content_owner = {}
    for content_owner in get_user_model().objects.filter(profile__registered_for="content_owner"):
        content_owner_data = {}
        content_owner_data['owner'] = {'name' : content_owner.company.name, 'id': content_owner.company.id }
        collections = []
        for collection in content_owner.collection.all():
            collection_data = {}
            if collection.id not in final_allowed_collections:
                continue
            collection_data['collection'] = {'name' : collection.name, 'id': collection.id }
            video_data = []
            for video in collection.video_set.all():
                video_dict = {}
                if video.id not in final_allowed_clips:
                    continue
                if video.video_url is None or video.video_url == '':
                    if video.video_file is not None:
                        video_dict['video_url'] = video.video_file.url
                    else:
                        video_dict['video_url'] = ''
                else:
                    video_dict['video_url'] = video.video_url
                video_dict['title'] = video.title
                video_dict['id'] = video.id
                video_dict['description'] = video.description
                if video.thumbnail != None:
                    video_dict['thumbnail'] = video.thumbnail.name
                else:
                    video_dict['thumbnail'] = '/static/company/images/videothumb.jpg'
                video_data.append(video_dict)
            collection_data['videos'] = video_data
            collections.append(collection_data)
        content_owner_data['collections'] = collections
        data.append(content_owner_data)
    return data