from django.shortcuts import render_to_response
from django.template import RequestContext


class render_to(object):

    def __init__(self, template=None):
        self._template = template

    
    def _get_template(self, func):

        if self._template is not None:
            return self._template

        path = '/'.join((m for m in func.__module__.split('.') if m != 'views'))

        return '%s/%s.html' % (path, func.__name__)

    def __call__(self, func):

        def wrapper(request, *args, **kwargs):
            template = self._get_template(func)            
            output = func(request, *args, **kwargs)
            assert isinstance(output, dict)
            return render_to_response(template, output, RequestContext(request))

        return wrapper
            
