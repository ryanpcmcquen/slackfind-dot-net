from django.template import Library
from django.contrib.auth.models import User

register = Library()

@register.inclusion_tag('lib/messages.html',takes_context=True)
def site_messages(context):
    return {
            'errors': context['request'].session.get('site_messages',{}).get('errors'),
            'notices': context['request'].session.get('site_messages', {}).get('notices')}
