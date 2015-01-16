
from os.path import join, dirname

from django.conf.urls.defaults import *

from django.contrib import admin

import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'packages.views.splash', name='splash'),
    url(r'^about/$', 'django.views.generic.simple.direct_to_template', {'template': 'about.html'}, name="about"),
    url(r'^packages/', include('packages.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin-media/(.*)$', 'django.views.static.serve', {'document_root': join(dirname(admin.__file__), 'media')}),
)
