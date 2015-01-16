# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User

from models import DistVersion, Package, SearchLog, Repository, Arch

from lib.widgets import MySelectMultiple
from packages.widgets import RepositorySelectWidget

class SearchForm(forms.Form):
    """
        simple form for search request
        in future need to split this form for two different
    """
    name = forms.CharField(max_length='32', min_length=2)
    distversion = forms.ModelChoiceField(queryset=DistVersion.objects.all(), required=False)
    
    def make_search_query(self):
        """
            returns queryset for current search state
        """
        if not self.is_valid():
            return None
        
        name = self.cleaned_data.get('name', '').lower().strip()
        query_kwargs = {'name__contains': name}
                        
        distversion = self.cleaned_data.get('distversion')
        
        if distversion:
            query_kwargs['distversion'] = distversion

        query_kwargs['visible'] = True
        
        SearchLog.objects.create(name=name.lower(), distversion=distversion)

        return Package.objects.filter(**query_kwargs)
        
class AdvancedSearchForm(SearchForm):
    """
        advanced form for search request
    """
    
    package_version = forms.CharField(max_length=32, required=False)
    repository = forms.ModelMultipleChoiceField(queryset=Repository.objects.exclude(default_mirror=None), 
                                                required=False, widget=RepositorySelectWidget)
    distversion = forms.ModelMultipleChoiceField(queryset=DistVersion.objects.all().order_by('-name'), required=False,
                                                 widget=MySelectMultiple)
    
    arch = forms.ModelMultipleChoiceField(queryset=Arch.objects.filter(active=True).order_by('name'), 
                                        widget=MySelectMultiple, required=False)

    location = forms.CharField(max_length=16, required=False)
    
    def check_for_exists(self, field):
        """
        checks one field for possible using in search query
        """
        return field in self.cleaned_data and len(self.cleaned_data[field]) > 0
            
    def make_search_query(self):
        """
            returns queryset for current search state 
        """
        name = self.cleaned_data.get('name')
        SearchLog.objects.create(name=name, distversion=None, advanced=True)

        query_kwargs = {'name__contains': name,}

        if self.check_for_exists('distversion'):
            query_kwargs['distversion__in'] = self.cleaned_data['distversion']
        
        if self.check_for_exists('repository'):
            query_kwargs['repository__in'] = self.cleaned_data['repository']

        if self.check_for_exists('arch'):
            query_kwargs['arch__in'] = self.cleaned_data['arch']

        if self.check_for_exists('package_version'):
            query_kwargs['version__contains'] = self.cleaned_data['package_version']

        if self.check_for_exists('location'):
            query_kwargs['location__contains'] = self.cleaned_data['location']
        
        query_kwargs['visible'] = True

        return Package.objects.filter(**query_kwargs)
        
