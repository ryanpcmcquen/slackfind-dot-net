
from django.conf import settings
from django.core.urlresolvers import reverse as native_reverse 
from django.utils.functional import memoize

from multilingual.languages import get_default_language_code

def reverse(*args, **kwargs):

    reversed_url = native_reverse(*args, **kwargs)

    if len(reversed_url) >= 2 and reversed_url[2] not in settings.NOT_LANG_URLS:
        return '/%s%s' % (get_default_language_code(), reversed_url)

    return reversed_url
