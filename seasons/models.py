from django.db import models
from pinax.apps.photos.models import Image
import datetime as dt


class SeasonManager(models.Manager):
    
    def get_season(self,d):
        ''' d is a datetime.date'''
        newd = dt.date(1976,d.month,d.day)
        for s in self.all():
            if newd > s.start and newd <= s.end:
                return s
    

class Season(models.Model):
    name = models.CharField(max_length=45)
    about = models.TextField()
    start = models.DateField()
    end = models.DateField()
    color = models.CharField(max_length=7) # HTML COLOR
    image = models.ForeignKey(Image,blank=True, null=True)
    objects = SeasonManager()
    
    def __unicode__(self):
        return self.name
    
    
            
        