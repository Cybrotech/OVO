from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
import json
from .models import Collection, Topic, Video, Country
from company.forms import CompanyRegistrationForm
from my_user.models import CustomUser
from company.models import UserProfile
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from website.models import Website, Section
from .email_messages import audience_registration_email, content_addition_email, request_widget_email
if "django_mailer" in settings.INSTALLED_APPS:
    from django_mailer import send_mail
else:
    from django.core.mail import send_mail
from website.static_class import MyNewClass
from .ajax_handle import get_video_duration


def register_audience(request):
    if request.user.is_authenticated():
        return redirect(reverse_lazy('add_content'))
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
            send_email_to_admins(user_name=user.first_name + ' ' + user.last_name)
            return redirect(reverse_lazy('login'))
    else:
        form = CompanyRegistrationForm()
    return render_to_response("register.html",
                  {'form': form}, context_instance=RequestContext(request))

def country_api(request):
    all_countries = Country.objects.all()
    js_countries = {'data': []}
    for each in all_countries:
        js_countries['data'].append(
            {
                "code": each.code,
                "name": each.name
            }
        )
    return HttpResponse(json.dumps(js_countries))

@login_required
@csrf_exempt
def add_content(request):
    if not request.user.is_superuser:
        if request.user.profile.registered_for == "website_owner":
            return redirect(reverse_lazy('add_website'))
        elif request.user.profile.registered_for == 'content_owner':
            pass
    parameters = {}
    parameters['ext'] = 'audience'
    parameters['section'] = 'audience'
    parameters['page'] = 'content'
    parameters['all_topics'] = Topic.objects.all()
    parameters['all_countries'] = Country.objects.all()
    parameters['error_messages'] = get_error_messages()
    new_obj = MyNewClass()
    # print 'firstone ', request.session['added_videos']
    if request.method == "POST":
        if request.session.get('post_video_req_count') is not None:
            request.session['post_video_req_count'] = request.session['post_video_req_count'] + 1
            if int(request.session['post_video_req_count'] == 1):
                del new_obj.added_videos[:]
                del new_obj.deleted_videos[:]
        myDict = dict(request.POST.iterlists())
        all_files = {}
        for key, value in request.FILES.iteritems():
            all_files[key] = value
        mytopic = Topic.objects.get(topic=myDict['topic_select'][0])
        mycollection, created = Collection.objects.get_or_create(
            name=myDict['collection'][0],
            user=request.user
        )
        mycollection.topic = mytopic
        mycollection.save()

        video_title_list = [k for k, v in myDict.iteritems() if k.startswith('video_title')]

        for each in video_title_list:
            video_url = myDict['video_url' + each[-2:]][0]
            video_file = all_files.get('video-select-' + each[-1])
            thumb_file = all_files.get('video-thumb-' + each[-1])

            blacklist_countries = myDict.get('blacklist_countries_' + each[-1])

            if video_file is not None:
                if myDict.get('video_path_' + each[-1]) is not None:
                    video_path = myDict['video_path_' + each[-1]][0]
                    myvideo, created = Video.objects.get_or_create(video_file=video_path)
                else:
                    myvideo = Video.objects.create(video_file=video_file)
                myvideo.title = myDict[each][0]
                myvideo.description = myDict['video_desc' + each[-2:]][0]
                myvideo.collection = mycollection
                thumb_present = False
                if thumb_file is not None:
                    myvideo.thumbnail = thumb_file
                    thumb_present = True
                myvideo.save()
                unique_video_src = myvideo.video_file.url
                abs_path = unique_video_src.replace('/media', '')
                abs_path = settings.MEDIA_ROOT + abs_path
                duration = get_video_duration(abs_path)
            else:
                myvideo = Video.objects.create(
                    title=myDict[each][0],
                    description=myDict['video_desc' + each[-2:]][0],
                    collection=mycollection,
                    video_url=video_url
                )
                if 'youtube.com' in video_url:
                    duration = get_video_duration(video_url)

                    url_split = video_url.split('=')
                    unique_video_src = 'https://www.youtube.com/embed/' + url_split[-1]
                elif 'vimeo.com' in video_url:
                    duration = '00:00:00'
                    url_split = video_url.split('/')
                    unique_video_src = '//player.vimeo.com/video/' + url_split[-1]
                else:
                    duration = '00:00:00'
                    unique_video_src = video_url
                thumb_present = False
                if thumb_file is not None:
                    myvideo.thumbnail = thumb_file
                    myvideo.save()
                    thumb_present = True
                
            if blacklist_countries is not None:
                for each_bl in blacklist_countries:
                    country_obj = Country.objects.get(code=each_bl)
                    myvideo.blacklisted_country.add(country_obj)

            myvideo_details = {
                'data': {
                    'title': myvideo.title,
                    'description': myvideo.description,
                    'video_path': unique_video_src,
                    'duration': duration,
                    'thumb_present': thumb_present
                }
            }

            common_list = [{'data': i['data']} for i in new_obj.added_videos]
            common_del_list = [{'data': i['data']} for i in new_obj.deleted_videos]
            if myvideo_details in common_list:
                myvideo.delete()
            elif  myvideo_details in common_del_list:
                myvideo.delete()
            else:
                myvideo_details['id'] = myvideo.id
                new_obj.added_videos.append(myvideo_details)

        video_titles = ', '.join(video_title_list)
        email_content = 'Videos: ' + video_titles + ' for ' + mycollection.name + ' collection'
        send_email_to_admins(content=email_content)
        if request.POST.get('redirect_field') == 'redirect':
            new_obj.clear()
            return redirect(reverse_lazy('add_content_audience'))
        else:
            parameters['added_videos'] = new_obj.added_videos
            # parameters['added_videos'] = request.session['added_videos']
            return render_to_response("addcontent.html", parameters, context_instance=RequestContext(request))
    else:
        new_obj.clear()
        request.session['post_video_req_count'] = 0
        # request.session['added_videos'] = []
        # request.session['deleted_videos'] = []
        # parameters['added_videos'] = new_obj.added_videos
        return render_to_response("addcontent.html", parameters, context_instance=RequestContext(request))


@login_required
def add_content_audience(request):
    if not request.user.is_superuser:
        if request.user.profile.registered_for == "website_owner":
            return redirect(reverse_lazy('add_website'))
        elif request.user.profile.registered_for == 'content_owner':
            pass    
    parameters = {}
    parameters['ext'] = 'audience'
    parameters['section'] = 'audience'
    parameters['page'] = 'content'
    if request.method == 'POST':
        myDict = dict(request.POST.iterlists())
        video_title_list = [k for k, v in myDict.iteritems() if k.find('video') != -1]

        section_title_list = [k for k, v in myDict.iteritems() if k.find('section') != -1]


        user_name = request.user.first_name + ' ' + request.user.last_name

        for each_section in section_title_list:
            section_obj = Section.objects.get(id=int(myDict[each_section][0]))
            section_obj.allowed_clips.clear()
            for each_clip in video_title_list:
                section_obj.allowed_clips.add(Video.objects.get(id=int(myDict[each_clip][0])))

        video_titles = [Video.objects.get(id=int(myDict[i][0])).title for i in video_title_list]
        section_titles = [Section.objects.get(id=int(myDict[i][0])).section_name for i in section_title_list]

        send_email_to_admins(
            user_name=user_name,
            content=', '.join(video_titles),
            sites=', '.join(section_titles)
        )
        return redirect(reverse_lazy('mail_confirmation_page'))



    # else:
    all_collections = Collection.objects.filter(user=request.user)
    final_collections = []
    for each in all_collections:
        data = {
            'collection': each
        }
        video_list = []
        videos = Video.objects.filter(collection=each)
        for each_vid in videos:
            vid_data = {
                'title': each_vid.title,
                'description': each_vid.description,
                'id': each_vid.id
            }
            if each_vid.video_url is None or each_vid.video_url == '':
                vid_orig_path = each_vid.video_file.url
                vid_data['video_path'] = '/' + '/'.join(vid_orig_path.split('/')[1:])
            else:
                vid_data['video_path'] = each_vid.video_url
            video_list.append(vid_data)
        data['videos'] = video_list
        final_collections.append(data)
    websites = Website.objects.all()
    final_websites = []
    for each_website in websites:
        data = {
            'website': each_website
        }
        sections = Section.objects.filter(website=each_website)
        data['sections'] = sections
        final_websites.append(data)
    parameters['collections'] = final_collections
    parameters['websites'] = final_websites
    return render_to_response("addcontentaudience.html", parameters, context_instance=RequestContext(request))


def collection_ajax(request):
    if request.user.is_authenticated():
        query = request.GET.get("term")
        collections = Collection.objects.filter(user=request.user, name__istartswith=query)
        mycollections = []
        for each in collections:
            mycollections.append({'label': each.name.upper(), 'value': each.name.upper()})
        return HttpResponse(json.dumps(mycollections))


# def generate_thumbnail(filename):
# Installation instructions 
# """sudo add-apt-repository ppa:jon-severinsson/ffmpeg
# sudo apt-get update
# sudo apt-get install ffmpeg"""
#     check_output(
#         'ffmpeg -i ' + filename + ' -ss 00:00:1.435 -f image2 -vframes 1 audience/static/images/out.png',
#         shell=True
#     )

def get_error_messages():
    error_messages = {
        'COLLECTION_TOPIC_EMPTY': settings.COLLECTION_TOPIC_EMPTY,
        'VIDEO_AND_URL_EMPTY': settings.VIDEO_AND_URL_EMPTY,
        'VIDEO_AND_URL_FILLED': settings.VIDEO_AND_URL_FILLED,
        'COLLECTION_AND_TYPE_EMPTY': settings.COLLECTION_AND_TYPE_EMPTY,
        'UNSUPPORTED_VIDEO_FORMAT': settings.UNSUPPORTED_VIDEO_FORMAT
    }
    return error_messages


def send_email_to_admins(user_name=None, content=None, sites=None):
    # instance = kwargs['instance']
    from_address = settings.DEFAULT_EMAIL_FROM_ADDRESS
    website_name = settings.WEBSITE_NAME
    if content is None:
        email_ready = audience_registration_email
    elif user_name is None:
        email_ready = content_addition_email
    else:
        email_ready = request_widget_email
    try:
        subject = email_ready["subject"]
        recipients = settings.ADMINS
        for recipient in recipients:
            if content is None:
                body = email_ready["body"] % (recipient[0], user_name, website_name)
            elif user_name is None:
                body = email_ready["body"] % (recipient[0], content, website_name)
            else:
                body = email_ready["body"] % (recipient[0], user_name, content, sites, website_name)
            send_mail(subject, body, from_address, [recipient[1]])
    except:
        return
