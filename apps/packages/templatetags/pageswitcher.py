# -*- coding: utf-8 -*-
"""
    Paginator templatetag wrapper
"""

from django import template
from lib.functions import get_params_from_request

register = template.Library()

@register.inclusion_tag('packages/templatetags/pageswitcher.html', takes_context=True)
def pageswitcher(context):
    """
        templatetag for display paging block
    """
    total = context.get('pages', 0)
    current = context.get('page', 1)
    
    if not isinstance(current, int):
        current = int(current) if current.isdigit() else 1

    pages = xrange(1, total)
    
    return {
            'get_params': '?%s&' % context['request'].META['QUERY_STRING'],
             'prev': current-1 if current > 1 else 1,
            'next': current+1 if current != total else total, 
            'showpaging': (total > 1), 
            'total': total,
            'pages': pages,
            'current': current,
             }
