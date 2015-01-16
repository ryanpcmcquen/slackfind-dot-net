"""
Purge existing packages metadata
"""


from django.core.management.base import BaseCommand

from packages.models import Package, Section, SearchLog

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        
        Package.objects.all().delete()
        SearchLog.objects.all().delete()
        Section.objects.update(checksum='', pc_checksum='')
        

