from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from .models import Collection, Topic, Video
from website.models import Website, WidgetFormatChoice, WidgetFormat
import subprocess
import ast
import os
from django.conf import settings
from website.static_class import MyNewClass, MyClass
from .video_duration import get_clip_duration, get_youtube_video_duration


class AjaxHandle():
    def save_collection(self, request):
        data = eval(request.POST.get('data'))
        if data is not None and data != "":
            mytopic = Topic.objects.get(topic=data['topic'])
            try:
                mycollection = Collection.objects.get(name=data['name'], user=request.user)
                mycollection.topic = mytopic
                mycollection.save()
            except:
                mycollection = Collection.objects.create(
                    name=data['name'],
                    topic=mytopic,
                    user=request.user
                )

        return HttpResponse(json.dumps({'status': 1}))

    def save_video_update(self, request):
        if(request.method == 'POST'):
            file = None
            for key, value in request.FILES.iteritems():
                file = value
            response_data = {'status': 0}

            data = dict(request.POST.lists())
            # data = ast.literal_eval(data)
            video_id = data['hidden-video-list-id'][0]
            video_title = data['hidden-video-list-title'][0]
            video_desc = data['hidden-video-list-desc'][0]
            myvideo = Video.objects.get(id=int(video_id))
            thumbnail_present = 0
            if file is not None:
                myvideo.thumbnail = file
                thumbnail_present = 1
            myvideo.title = video_title
            myvideo.description = video_desc
            myvideo.save()
            response_data = {'status': 1, 'thumbnail_present': thumbnail_present, 'title': video_title}
            return HttpResponse(json.dumps(response_data))
        else:
            return HttpResponse(json.dumps({'status': 0}))

    def save_video(self, request):
        if(request.method == 'POST'):
            file = None
            for key, value in request.FILES.iteritems():
                file = value
            response_data = {'status': 0}
            if file is not None:
                myvideo = Video.objects.create(
                    video_file=file,
                )
                video_path = myvideo.video_file.url
                myvideo.delete()
                duration = get_video_duration(video_path)
                video_path = '/media/' + video_path.split('/')[-1]
                response_data = {'status': 1, 'video_id': myvideo.id, 'duration': duration, 'video_path': video_path}

            else:
                # no file
                data = dict(request.POST.lists()).get('data')[0]
                data = ast.literal_eval(data)
                youtube_video_url = data['video_path']

                duration = get_video_duration(youtube_video_url)
                response_data = {'status': 1, 'duration': duration}
            return HttpResponse(json.dumps(response_data))
        else:
            return HttpResponse(json.dumps({'status': 0}))

    def delete_video(self, request):
        data = dict(request.POST.lists()).get('data')[0]
        data = ast.literal_eval(data)
        if data is not None and data != "":
            video_path = data['video_path']
            if int(data['video_id']) != -1:
                delete_video = Video.objects.get(id=int(data['video_id']))
                delete_video.delete()

                static_obj = MyNewClass()
                if len(static_obj.added_videos)>0:
                    # find and remove entry from list
                    for each_vid in static_obj.added_videos:
                        if each_vid['id'] == int(data['video_id']):
                            # entry to be removed is each_vid
                            static_obj.added_videos.remove(each_vid)
                            static_obj.deleted_videos.append(each_vid)


                # if len(request.session['added_videos'])>0:
                #     # find and remove entry from list
                #     for each_vid in request.session['added_videos']:
                #         if each_vid['id'] == int(data['video_id']):
                #             # entry to be removed is each_vid
                #             request.session['added_videos'].remove(each_vid)
                #             request.session['deleted_videos'].append(each_vid)
                #             print 'video removed from added_videos and added to deleted_videos'

            video_path = data['video_path'].replace('/media', '')
            video_path = settings.MEDIA_ROOT + video_path
            try:
                os.remove(video_path)
            except:
                pass
            return HttpResponse(json.dumps({'status': 1}))
        else:
            return HttpResponse(json.dumps({'status': 0}))

    def delete_website(self, request):
        data = dict(request.POST.lists()).get('data')[0]
        data = ast.literal_eval(data)
        if data is not None and data != "":
            url = data['url']
            website_obj = Website.objects.get(url=url, user=request.user)
            static_obj = MyClass()
            if len(static_obj.added_websites)>0:
                # find and remove entry from list
                for each_site in static_obj.added_websites:
                    print each_site
                    print website_obj.id
                    if each_site['website'].id == website_obj.id:
                        # entry to be removed is each_vid
                        static_obj.added_websites.remove(each_site)
            website_obj.delete()
            return HttpResponse(json.dumps({'status': 1}))
        else:
            return HttpResponse(json.dumps({'status': 0}))

    def get_video_duration(self, request):
        data = dict(request.POST.lists()).get('data')[0]
        data = ast.literal_eval(data)
        if data is not None and data != "":
            if 'youtube.com' in data['video_path']:
                video_path = data['video_path']
            else:
                video_path = data['video_path'].replace('/media', '')
                video_path = settings.MEDIA_ROOT + video_path
            duration = get_video_duration(video_path)
            # duration = get_video_duration('audience' + data['video_path'])
            return HttpResponse(json.dumps({'status': 1, 'duration': duration}))
        else:
            return HttpResponse(json.dumps({'status': 0}))

    def set_widgetformat_size(self, request):
        data = dict(request.POST.lists()).get('data')[0]
        data = ast.literal_eval(data)
        if data is not None and data != "":
            widget_name = data['widget_name']
            widget_size = data['widget_size']
            if widget_size !='undefined':
                widget_format_obj = WidgetFormat.objects.get(name=widget_name, is_enabled=True)
                try:
                    widget_format_choice = WidgetFormatChoice.objects.get(
                        widget_format=widget_format_obj,
                        user=request.user
                    )
                except:
                    widget_format_choice = WidgetFormatChoice.objects.create(
                        size=widget_size,
                        user=request.user,
                        widget_format=widget_format_obj
                    )
                widget_format_choice.size = widget_size
                widget_format_choice.save()
            return HttpResponse(json.dumps({'status': 1}))
        else:
            return HttpResponse(json.dumps({'status': 0}))                


@csrf_exempt
def ajax_request(request, func_name):
    ajax_handle = AjaxHandle()
    return_msg = getattr(ajax_handle, func_name)(request)
    return return_msg


def get_video_duration(filename):
    """
    Returns duration of a video file
    """
    if 'youtube.com' in filename:
        duration = get_youtube_video_duration(filename)
    else:
        duration = get_clip_duration(filename)
    # try:
    #     result = subprocess.Popen(
    #         ["ffprobe", filename],
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.STDOUT
    #     )
    #     duration_line = [x for x in result.stdout.readlines() if "Duration" in x]
    #     duration = duration_line[0].split(',')[0][-11:-3]
    # except:
    #     duration = "00:00:00"
    return duration
