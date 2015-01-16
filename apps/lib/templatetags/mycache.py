from django.template import Library, Node, TemplateSyntaxError, Variable, VariableDoesNotExist
from django.template import resolve_variable
from django.core.cache import cache
from django.utils.encoding import force_unicode

register = Library()

class CacheNode(Node):
    def __init__(self, nodelist, expire_time_var, cache_key):
        self.nodelist = nodelist
        self.expire_time_var = Variable(expire_time_var)
        self.cache_key = cache_key

    def render(self, context):
        try:
            expire_time = self.expire_time_var.resolve(context)
        except VariableDoesNotExist:
            raise TemplateSyntaxError('"cache" tag got an unknkown variable: %r' % self.expire_time_var.var)
        try:
            expire_time = int(expire_time)
        except (ValueError, TypeError):
            raise TemplateSyntaxError('"cache" tag got a non-integer timeout value: %r' % expire_time)
        # Build a unicode key for this fragment and all vary-on's.
        cache_key = resolve_variable(self.cache_key, context)
        value = cache.get(cache_key)
        if value is None:
            value = self.nodelist.render(context)
            cache.set(cache_key, value, expire_time)
        return value

def do_cache(parser, token):
    """
    This will cache the contents of a template fragment for a given amount
    of time.

    Usage::
    This tag also supports varying by a list of arguments::

        {% load cache %}
        {% cache [expire_time] [variable] .. %}
            .. some expensive processing ..
        {% endcache %}

    Each unique set of arguments will result in a unique cache entry.
    """
    nodelist = parser.parse(('endsimplecache',))
    parser.delete_first_token()
    tokens = token.contents.split()
    if len(tokens) < 3:
        raise TemplateSyntaxError(u"'%r' tag requires at least 2 arguments." % tokens[0])
    return CacheNode(nodelist, tokens[1], tokens[2])

register.tag('simplecache', do_cache)
