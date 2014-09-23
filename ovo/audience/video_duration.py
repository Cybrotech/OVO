from hachoir_core.error import HachoirError
from hachoir_core.cmd_line import unicodeFilename
from hachoir_parser import createParser
from hachoir_core.tools import makePrintable
from hachoir_metadata import extractMetadata
from hachoir_core.i18n import getTerminalCharset
from sys import argv, stderr, exit

from datetime import timedelta
from urllib2 import urlopen
from xml.dom.minidom import parseString


def get_clip_duration(filename):
    filename, realname = unicodeFilename(filename), filename
    parser = createParser(filename, realname)
    if not parser:
        print >>stderr, "Unable to parse file"
        exit(1)
    try:
        metadata = extractMetadata(parser)
    except HachoirError, err:
        print "Metadata extraction error: %s" % unicode(err)
        metadata = None
    if not metadata:
        print "Unable to extract metadata"
        exit(1)

    duration = metadata.get('duration')
    seconds = duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    duration = str("%02d" % hours) + ':' + str("%02d" % minutes) + ':' + str("%02d" % seconds)
    return duration

def get_youtube_video_duration(url):
    video_url = url.split('=')[-1]
    url = 'https://gdata.youtube.com/feeds/api/videos/{0}?v=2'.format(video_url)
    s = urlopen(url).read()
    d = parseString(s)
    e = d.getElementsByTagName('yt:duration')[0]
    a = e.attributes['seconds']
    v = int(a.value)
    t = timedelta(seconds=v)

    seconds = t.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    duration = str("%02d" % hours) + ':' + str("%02d" % minutes) + ':' + str("%02d" % seconds)
    return duration

# print get_youtube_video_duration('https://www.youtube.com/watch?v=eN9XX-dd0LQ')
# print get_clip_duration('/home/santosh/abc.mp4')