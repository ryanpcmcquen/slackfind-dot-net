# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from packages import models 
from packages.downloaders import download_section_metadata
from packages.parsers import Section_Parser

class Command(BaseCommand):
    
    def handle(self, *args, **options):

        for section in models.Section.objects.filter(crawl=True):
            if section.repository.crawl:
                print section
                s = Section_Parser(section, download_section_metadata(section))
                s.parse()
                del s

        from django.core.cache import cache
        from django.conf import settings
            
        for key, name in settings.LANGUAGES:
            cache.delete('statcache-' + key);
        
