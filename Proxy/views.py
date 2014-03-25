from django.http import HttpResponse
from Proxy import ProxyCache as FastCache
from django.shortcuts import render
from os import environ
from ReverseProxy import conf
import urllib2
import mimetypes
import urllib
import cookielib
import pickle
import hashlib

# Create your views here.
PROXY_URL = conf.PROXY_URL
OUR_URL = conf.OUR_URL


def index(request):
    #process URL
    path = request.get_full_path()  #.replace('/proxy', '')
    real_path = PROXY_URL + path

    #process MIME
    remote_mime = mimetypes.guess_type(real_path)
    remote_mime = remote_mime[0]

    if remote_mime == 'application/php':
        remote_mime = ''
    else:
        pass

    if remote_mime:
        if remote_mime.startswith('image') or remote_mime.startswith('application/javascript'):
            cache_key = remote_mime + '-' + hashlib.md5(remote_mime).hexdigest().upper()
        else:
            cache_key = 'none'
    else:
        cache_key = 'none'

    if (not FastCache.check_cache(cache_key)) and (not cache_key == 'none'):
        remote_content = FastCache.get_cache(cache_key)
        if remote_content:
            return HttpResponse(remote_content, content_type=remote_mime)

    print cache_key
    print remote_mime, path

    #process POST
    dict = {}
    for (k, v) in request.POST.items():
        print "dict[%s]=" % k, v
        dict[k] = v.encode("utf-8")


    #process COOKIES
    cookie_path = r"./cookies.txt"
    cookies = cookielib.MozillaCookieJar(cookie_path)

    if request.COOKIES.has_key("cookie"):
        cookies_str = pickle.loads(request.COOKIES["cookie"])
        cookies._cookies = cookies_str

    try:
        cookies.load(ignore_discard=True, ignore_expires=True)
    except Exception:
        pass
        #print Exception.message

    #process Request
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    data = urllib.urlencode(dict)
    req = urllib2.Request(real_path, data=data)

    #todo process request._files
    #req.add_data(files)
    #process Remote_Response
    remote_response = opener.open(req)
    remote_content = remote_response.read().replace(PROXY_URL, OUR_URL)
    response = HttpResponse(remote_content, content_type=remote_mime)

    #save COOKIES
    if request.method == 'POST':
        cookies.extract_cookies(remote_response, req)
        cookies_str = pickle.dumps(cookies._cookies)
        response.set_cookie("cookie", cookies_str)

        # cookies.save(cookiefile, ignore_discard=True, ignore_expires=True)

    #FastCache
    if not cache_key == 'none':
        FastCache.set_cache(cache_key, remote_content)

    return response