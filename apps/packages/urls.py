from django.conf.urls.defaults import *

urlpatterns = patterns('packages.views',
                       url(r'^search/$', 'search', name="search"),
                       url(r'^search/advanced/$', 'advanced_search', name="advanced-search"),
                       url(r'^choosemirror/(?P<package_id>\d+)/$', 'choose_mirror', name="choose-mirror-by-id"),
                       url(r'^choosemirror/(?P<section_id>\d+)/(?P<name>.*)/(?P<version>.*)/(?P<arch_name>.*)/(?P<build>.*)/$', 'choose_mirror_by_params', name="choose-mirror-by-params"),
                       url(r'^repositories/', 'repository_list', name="repository-list")
                       )
