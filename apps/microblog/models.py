from django.db import models 
from django.utils.translation import ugettext_lazy as _

from multilingual.translation import TranslationModel

class Post(models.Model):
    
    pub_date = models.DateField(auto_now_add=True)
    posted_by = models.CharField(max_length=16)
    
    class Translation(TranslationModel):        
        text = models.CharField(max_length=256)
        
    def __unicode__(self):
        return self.pub_date.isoformat() 
        
    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ['-pub_date', '-id']
