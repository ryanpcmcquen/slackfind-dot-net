# -*- coding: utf-8 -*-

from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.vary import vary_on_headers

from packages.decorators import render_to
from packages.forms import SearchForm, AdvancedSearchForm
from packages import settings
from packages.models import Package, Mirror, Section, Arch

def search_base(request, form_class, extra_context=None):
    """
    base search view for all search queries, just put search form into 
    template and returns needed context dictionary
    """
    if extra_context is None:
        extra_context = {}
    
    form = form_class(request.GET.copy())
    form_valid = form.is_valid()
    if not form_valid :
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    
    paginator = Paginator(form.make_search_query(), 
                          settings.SEARCH_RESULT_PERPAGE)
    num_page = request.GET.get('page', 1)
    
    context = {
            'result': paginator.page(num_page),
            'page': num_page,
            'pages': paginator.num_pages,
            'objects_count': paginator.count,
            'form_valid': form_valid,
            'search_name': request.GET.get('name'),
            }
    
    context.update(extra_context)
    return context


@render_to('packages/search.html')
def advanced_search(request):
    return search_base(request, AdvancedSearchForm, {'advanced_form': True})


@render_to
def search(request):
    return search_base(request, SearchForm) 

@vary_on_headers('User-Agent', 'Cookie')
def splash(request, *args, **kwargs):
    """
    index page view
    """
    from django.views.generic.simple import direct_to_template
    from multilingual.languages import get_default_language_code
    
    from microblog.models import Post 
    from packages.models import SearchLog

    if 'extra_context' not in kwargs:
        kwargs['extra_context'] = {}

    extra_context = {}
    extra_context['blog_posts'] = lambda: Post.objects.all()[:5]
    extra_context['top_search'] = SearchLog
    extra_context['statcache'] = 'statcache-' + get_default_language_code() 
    extra_context['blogcache'] = 'splashblogcache-'+ get_default_language_code()
    
    kwargs['extra_context'].update(extra_context)

    return direct_to_template(request, 'packages/splash.html', *args, **kwargs)
    
@render_to
def choose_mirror(request, package_id, *args, **kwargs):
    """
    choose one mirror by package 
    """
    
    package = get_object_or_404(Package, id=package_id)
    
    mirrors = []
    
    for mirror in Mirror.objects.filter(repository=package.repository):
        mirrors.append({'mirror':mirror, 'link': package.download_link(mirror)})
    
    return {'mirrors': mirrors, 
            'package': package,}
   

@render_to('packages/choose_mirror.html')
def choose_mirror_by_params(request, section_id, name, version, arch_name, build):
    
    section = get_object_or_404(Section, id=section_id)
    arch = get_object_or_404(Arch, name=arch_name)
    package = get_object_or_404(Package, section=section, name=name, version=version, arch=arch, build=build)

    mirrors = []
    
    for mirror in Mirror.objects.filter(repository=package.repository):
        mirrors.append({'mirror':mirror, 'link': package.download_link(mirror)})
   
    return {'mirrors': mirrors, 'package': package}


@render_to
def repository_list(request):
    """
    list of all repositories for statistics
    """
    from packages.models import Repository
    return {'object_list': Repository.objects.all()}

