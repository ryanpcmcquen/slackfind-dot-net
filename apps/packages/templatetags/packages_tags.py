# -*- coding: utf-8 -*-

from django import template
from django.conf import settings

from packages.models import Package, Repository, Mirror
from packages.forms import SearchForm, AdvancedSearchForm

register = template.Library()

@register.inclusion_tag('packages/templatetags/download.html')
def download(user, package):
    """
        templatetag for download one package
    """
    
    return {'package': package,}

@register.inclusion_tag('packages/templatetags/search.html', takes_context=True)
def search(context):
    
    if 'search_form' not in context:
        if 'request' in context:
            form = SearchForm(context['request'].GET.copy())
        else:
            form = SearchForm()
        
    else:
        form = context['form']
    
    is_advanced_form = 'advanced_form' in context

    if 'advanced_search_form' not in context:   
        if 'request' in context:
            advanced_form = AdvancedSearchForm(context['request'].GET.copy())
        else:
            advanced_form = AdvancedSearchForm()
    else:
        advanced_form = context['advanced_search_form']
            
    return {'search_form': form, 'advanced_search_form': advanced_form, 'is_advanced_form': is_advanced_form,
            'settings': settings}

@register.inclusion_tag('packages/templatetags/stats.html')
def stats():
    """
        templatetag for main page
    """
    data = {}
    data['repositories'] = Repository.objects.exclude(default_mirror=None).count()
    data['mirrors'] = Mirror.objects.filter(available=True).count()
    data['packages'] = Package.objects.filter(visible=True).count()
    data['size_compressed'], data['size_uncompressed'] = Package.sum_sizes()
    
    return data

@register.simple_tag
def repositorylink(obj):

    
    if isinstance(obj, int):

        try:
            repository = Repository.objects.get(pk=obj)
        except Repository.DoesNotExist:
            return ''

    else:
        repository = obj

    return '<span>%s <a href="%s" rel="nofollow" class="arrow">&nbsp;&nbsp;&nbsp;&nbsp;</a></span>' % (repository, repository.get_absolute_url(),)


@register.inclusion_tag('packages/templatetags/related_packages.html')
def related_packages(source_string):

    result = []

    for group in source_string.split('|'):
        result.append( (package.strip().split(' ')[:2] + package.split(' ')[2].rsplit('-', 3) for package in group.strip().split(',')) )
                
    return {'data': result}
    

