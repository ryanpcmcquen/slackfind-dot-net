# -*- coding: utf-8 -*-
"""
    Models of packages application
"""

from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

class Arch(models.Model):
    name = models.CharField(_('name'), max_length=16, unique=True, db_index=True)
    active = models.BooleanField(_('active'), default=False)

    def __unicode__(self):
        return self.name

class Package(models.Model):
    """
        package model
    """
    section = models.ForeignKey('Section', verbose_name=_('section'))
    distversion = models.ForeignKey('DistVersion', verbose_name=_('version'))
    repository = models.ForeignKey('Repository', verbose_name=_('repository'))
    
    name = models.CharField(_('name'), max_length=128, db_index=True)
    description = models.TextField(_('Description'), null=True, blank=True)
    size_compressed = models.PositiveIntegerField(_('package size'), default=0)
    size_uncompressed = models.PositiveIntegerField(_('package programm'), default=0)
    requires = models.TextField(_('dependencies'), null=True, blank=True)
    conflicts = models.TextField(_('conflicts'), null=True, blank=True)
    suggests = models.TextField(_('suggests'), null=True, blank=True)

    version = models.CharField(_('version'), max_length=64, db_index=True)
    build = models.CharField(_('build'), max_length=32)
    location = models.CharField(_('path'), max_length=64, db_index=True)
    visible = models.BooleanField(_('visibility'), default=True, db_index=True)

    arch = models.ForeignKey(Arch, verbose_name=_('arch'))

    extension = models.CharField(_('extension'), max_length=4, default='txz', db_index=True)
    pc_checksum = models.CharField(_('package control checksum'), max_length=32)

    def __unicode__(self):
        return self.raw_name

    class Meta:
        verbose_name = _('package')
        verbose_name_plural = _('packages')
        #ordering = ['name',]

    @staticmethod
    def sum_sizes():
        """
            returns size of packages
        """
        compressed = 0
        uncompressed = 0

        for p in Package.objects.filter(visible=True):
            compressed += p.size_compressed
            uncompressed += p.size_uncompressed

        return (float(compressed)/1048576, float(uncompressed)/1048576)
    
    def save(self, *args, **kwargs):
        """
        Overridden for always strip and remove ./ in head
        """
        self.location = unicode(self.location).strip()
        
        if self.location[:2] == './':
            self.location = self.location[2:]

        super(Package, self).save(*args, **kwargs)
        
    
    def download_link(self, mirror=None):
        
        if not isinstance(mirror, Mirror): # is None check already here
            url = self.repository.default_mirror.url
        else:
            url = mirror.url
        
        location = self.location[2:] if self.location[:2] == './' else self.location
        return '%s%s%s/%s.%s' % (url, self.section.path, location, unicode(self), self.extension)
    
    @property
    def default_download_link(self):

        return self.download_link(self.repository.default_mirror)

    def set_raw_name(self, value):

        value = value.strip()

        new_value_tuple = value.rsplit('.', 1)
        self.name, self.version, arch, self.build = new_value_tuple[0].rsplit('-', 3)
        
        arch, c = Arch.objects.get_or_create(name=arch)

        if c:
            raise ValueError('Unknown Arch')

        self.arch = arch

        self.extension = new_value_tuple[1]

    def get_raw_name(self, value=None):

        if value is None:
            return '%s-%s-%s-%s' % (self.name, self.version, self.arch, self.build)

    raw_name = property(get_raw_name, set_raw_name)

    @property
    def relation_key(self):
        return 'package_relation_%d' % self.id

class Section(models.Model):
    """
        One section iside repository (ex. distributive version in one repository)
    """
    repository = models.ForeignKey('Repository', verbose_name=_('repository'))
    distversion = models.ForeignKey('DistVersion', verbose_name=_('version'))
    path = models.CharField(_('path from root'), max_length=64)
    
    crawl = models.BooleanField(u'Флаг сбора пакетов', default=True, 
                                    db_index=True)
    
    #here is md5 checksum of data repository
    checksum = models.CharField(_('metadata checksum'), null=True, blank=True, max_length=32)

    pc_checksum = models.CharField(_('package control checksum'), null=True, blank=True, max_length=32)

    def __unicode__(self):
        return '%s - %s' % (self.repository, self.path)
    
    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')
        
    def get_absolute_path(self):
        """
            returning absolute path to dist version repository
        """
        if not self.repository.default_mirror:
            return None

        return self.repository.default_mirror.url + self.path

    def get_absolute_url(self):
        return self.get_absolute_path()

    def make_pc_checksum(self):
        
        from hashlib import md5
        from datetime import datetime

        self.pc_checksum = md5(datetime.now().isoformat() + self.get_absolute_path()).hexdigest()
        self.save()

        return self.pc_checksum

    def cleanup_deprecated_packages(self):
         
        qset = Package.objects.filter(section=self).exclude(pc_checksum=self.pc_checksum)
        count = qset.count()
        qset.delete()

        return count 


class Mirror(models.Model):
    """
        mirror of one repository
    """
    url = models.URLField(u'URL', verify_exists=False)
    repository = models.ForeignKey('Repository', verbose_name=_('repository'))
    
    available = models.BooleanField(_('available'), default=True, db_index=True)    
    alive = models.BooleanField(_('alive'), default=False, db_index=True)

    def section_path_iter(self, *args, **kwargs):
        return (self.url + section.path for section in Section.objects.filter(repository=self.repository, *args, **kwargs))
            
    def __unicode__(self):
        return self.url

    class Meta:
        verbose_name = _('mirror')
        verbose_name_plural = _('mirrors')


    
class Repository(models.Model):
    """
        Repository of packages (ex. slacky.eu, linuxpackages.net, slackware.com)
    """
    name = models.CharField(u'Имя', max_length=255)
    default_mirror = models.ForeignKey(Mirror, null=True, blank=True,
                                        related_name='default_mirror')

    encoding = models.CharField(_('Codepage PACKAGES.TXT'),
                                 max_length=16, default='utf-8')

    url = models.URLField(_('url'), verify_exists=False, null=True, blank=True)

    crawl = models.BooleanField(_('flag collect packages'), default=True)   

    def get_available_mirrors(self):
        return Mirror.objects.filter(available=True, repository=self)


    @property
    def more_than_one_mirror(self):
        """
        this method made for template where we cannot make queryset and check
        """
        return (Mirror.objects.filter(repository=self, available=True).count() > 1)

    @property
    def count_mirrors(self):
        return Mirror.objects.filter(repository=self, available=True).count()
    
    @property
    def count_packages(self):
        return Package.objects.filter(repository=self).count()

    class Meta:
        verbose_name = _('repository')
        verbose_name_plural = _('repositories')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.url or 'http://%s' % self.name

class SubRepository(models.Model):
    """
        SubRepository, special for slackware.com repository (testing, unstable ect)
    """
    path = models.CharField(u'Путь', max_length=16)
    repository = models.ForeignKey(Repository)

    def __unicode__(self):
        return self.path

class DistVersion(models.Model):
    """
        one dist version 
    """
    name = models.CharField(_('verbose name'), max_length=32)

    class Meta:
        verbose_name = _('version')
        verbose_name_plural = _('versions')

    def __unicode__(self):
        return self.name


class SearchLog(models.Model):
    """
        model for logging search matches
    """

    name = models.CharField(_('name'), max_length=128, db_index=True)
    distversion = models.ForeignKey(DistVersion, verbose_name=_('version'), null=True)
    advanced = models.BooleanField(_('advanced search'), default=False)
    user = models.ForeignKey(User, null=True)
    when = models.DateTimeField(_('query time'), auto_now_add=True, null=True, blank=True)
    
    @staticmethod
    def top():
        """
        TODO: Make own manager
        """

        import random
        
        from django.db import connection

        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) AS cnt, name FROM packages_searchlog GROUP BY name ORDER BY cnt DESC LIMIT 25")
        
        i = 1

        result = [] 

        for count, name in cursor.fetchall():
            i += 1
            result.append( {'count': count, 'name': name, 'position': i/2} )

        random.shuffle(result)

        return result

