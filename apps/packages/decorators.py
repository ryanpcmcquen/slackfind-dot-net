from django.shortcuts import render_to_response
from django.template import RequestContext


def render_to(template):
    """
        this decorator makes more easy render of page to template
    """
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if not isinstance(output, dict):
                return output
            else:
                return render_to_response(template, output, \
                        RequestContext(request))
        return wrapper

    if callable(template):
        fn = template
        path = ''
        for module in template.__module__.split('.'):
            if module != 'views':
                path += module + '/'
        
        template = "%s%s.html" % (
            path,
            template.__name__
        )
        return renderer(fn)
    return renderer
