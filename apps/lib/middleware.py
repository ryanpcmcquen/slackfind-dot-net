"""
Multilingual middleware: choosing language
"""

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.utils.translation import check_for_language, get_language_from_request

from multilingual.languages import get_default_language_code, get_language_code, \
    set_default_language, get_default_language

class MultilingualMiddleware(object):

    def process_request(self, request):
        
        from django.utils import translation
                
        path_tuple = request.path_info.split("/")
        
        if len(path_tuple) > 1:
            
            if path_tuple[1] in settings.NOT_LANG_URLS:
                return
        
            if check_for_language(path_tuple[1]):
                
                lang = path_tuple[1]
                
                if hasattr(request, 'session'):
                    request.session['django_language'] = lang
                
                request.COOKIES['django_language'] = lang
            
                set_default_language(lang)
                request.path_info = "/" + "/".join(path_tuple[2:])                
                return
        
        if hasattr(request, "session") and "django_language" in request.session:
            lang = request.session["django_language"]
        elif hasattr(request, "COOKIE") and "django_language" in request.COOKIE:
            lang = request.COOKIE["django_language"]
        elif check_for_language(get_language_from_request(request)):
            set_default_language(get_language_from_request(request))
            lang = get_language_from_request(request)
        else:
            lang = settings.LANGUAGES[settings.DEFAULT_LANGUAGE][0]
            
        return HttpResponseRedirect('/%s%s' % (lang, request.path_info))

