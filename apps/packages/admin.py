# -*- coding: utf-8 -*-

from django.forms import ModelChoiceField
from django.contrib import admin

from models import Repository, DistVersion, Mirror, Package, Section, SubRepository, Arch

class DistVersionAdmin(admin.ModelAdmin):
    pass

class MirrorAdmin(admin.ModelAdmin):
    list_display = ['url', 'repository', 'available',]
    list_filter = ['repository',]

class PackageAdmin(admin.ModelAdmin):
    pass

class SectionAdmin(admin.ModelAdmin):
    list_display = ['repository', 'distversion', 'crawl']
    list_filter = ['repository',]
    
class SubRepositoryAdmin(admin.ModelAdmin):
    list_display = ['repository', 'path']

class ArchAdmin(admin.ModelAdmin):
    list_display = ['name', 'active',]
    
class SectionInline(admin.TabularInline):    
    model = Section    
    extra = 7
    
class SubRepositoryInline(admin.TabularInline):
    model = SubRepository    
    
class MirrorInline(admin.TabularInline):
    model = Mirror    
    
class RepositoryAdmin(admin.ModelAdmin):
    
    inlines = [
                SectionInline,
                SubRepositoryInline,
                MirrorInline,
               ]

admin.site.register(Repository, RepositoryAdmin)
admin.site.register(SubRepository, SubRepositoryAdmin)
admin.site.register(DistVersion, DistVersionAdmin)
admin.site.register(Mirror, MirrorAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Arch, ArchAdmin)
