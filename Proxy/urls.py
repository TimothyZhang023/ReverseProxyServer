from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('Proxy.views',
    # Examples:
    # url(r'^$', 'ReverseProxy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
     url(r'$', 'index', name='index'),

   # url(r'^admin/', include(admin.site.urls)),
)
