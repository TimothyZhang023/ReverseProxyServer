from django.http import HttpResponse
from django.shortcuts import render
from os import environ
from ReverseProxy import conf
import urllib2
import mimetypes
import urllib
import cookielib
# Create your views here.
PROXY_URL = conf.PROXY_URL
OUR_URL = conf.OUR_URL
kv = ''
is_sae = environ.get("APP_NAME", "")
if not is_sae:
    cookie_path = r"./cookies.txt"
    cookie_url = r"./cookies.txt"

else:
#SAE
    from sae.ext.storage import monkey
    import sae.kvdb

    monkey.patch_all()
    cookie_path = r"/s/cookie/cookies.txt"
    cookie_url = r'http://reverseproxy4py-cookie.stor.sinaapp.com/cookies.txt'

    kv = sae.kvdb.KVClient()



def index(request):
    if is_sae and  kv.get('cookie') == '':
        kv.set('cookie', 'init')
        
    path = request.get_full_path()  #.replace('/proxy', '')

    real_path = PROXY_URL + path

    # print real_path

    mime = mimetypes.guess_type(real_path)
    mime = mime[0]

    if mime == 'application/php':
        mime = ''
    else:
        pass
        # print mime

    print mime,path
    params_POST = request.POST

    dict = {}
    for (k, v) in params_POST.items():
        print "dict[%s]=" % k, v
        dict[k] = v.encode("utf-8")
        #.encode("utf-8")

    params_files = request._files



    # Cookie_handler = urllib2.HTTPCookieProcessor()
    # req = urllib2.build_opener(Cookie_handler)
    # urllib2.install_opener(req)
    cookiefile = cookie_path
    cookies = cookielib.MozillaCookieJar(cookie_url)
    if is_sae:
        cookies._cookies = kv.get("cookie")

    try:
        cookies.load(ignore_discard=True, ignore_expires=True)
    except Exception:
        print Exception.message

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))

    data = urllib.urlencode(dict)

    req = urllib2.Request(real_path, data=data)

    #req.add_header('Cookie', value)

    response = opener.open(req)

    content = response.read().replace(PROXY_URL, OUR_URL)

    if request.method == 'POST':
        cookies.extract_cookies(response, req)
        cookies.save(cookiefile, ignore_discard=True, ignore_expires=True)

    if is_sae:
        kv.set('cookie', cookies._cookies)

    return HttpResponse(content, content_type=mime)#, content_type="application/json"