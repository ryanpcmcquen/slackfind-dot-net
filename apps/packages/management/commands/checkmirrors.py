from __future__ import with_statement

from django.core.management.base import BaseCommand

from packages.models import Mirror
from packages.functions import check_url_for_alive

class Command(BaseCommand):
    """
        command for check one mirror to dead or alive
    """
    def handle(self, *args, **options):

        for mirror in Mirror.objects.filter(available=True):
            for mirror_path in mirror.section_path_iter(crawl=True):
                mirror.alive = check_url_for_alive(mirror_path + 'PACKAGES.TXT')
                mirror.save()
                    
        
