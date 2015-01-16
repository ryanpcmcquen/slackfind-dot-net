# -*- coding: utf-8 -*-

from django.forms import widgets 
from django.template import loader, Context

class MySelectMultiple(widgets.SelectMultiple):
    
    def render(self, name, value, *args, **kwargs):
        
        if not isinstance(name, (unicode, str)):
            raise ValueError('name should be string or unicode')

        template_name = kwargs.get('template_name') or 'lib/widgets/my_select_multiple.html'

        t = loader.get_template(template_name)
        
        if value is None:
            value = []

        data = []
        for idx, choice in self.choices:
            data.append({
                         'value': choice,
                         'idx': idx,
                         'checked': unicode(idx) in value, 
                         })
        
        context = Context({
                          'name': name,
                          'data': data, 
                           })
        
        return t.render(context)
    
