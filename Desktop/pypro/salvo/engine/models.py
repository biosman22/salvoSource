
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from datetime import datetime   

from  urllib.request import urlopen
from urllib.error import HTTPError

class downloaded(models.Model):
    file_name       = models.CharField( max_length = 200,)
    content_type    = models.CharField( max_length = 50,)
    up_date         = models.DateTimeField(default = datetime.now, blank=True)
    task_id         = models.CharField( max_length = 200,)
    unique_id       = models.CharField( max_length = 200, default = None)
    def setup(self, File_Name, Content_Type, Up_Date, Task_Id, Unique_Id):
        self.file_name    = File_Name
        self.up_date      = Up_Date
        self.task_id      = Task_Id
        self.content_type = Content_Type
        self.unique_id    = Unique_Id
        
def get_img(unique_id):
    """Return the pathname of the KOS root directory."""
    try:
        urlopen("http://i.ytimg.com/vi/"+unique_id+"/maxresdefault.jpg")
        return str("http://i.ytimg.com/vi/"+unique_id+"/maxresdefault.jpg") 

    except HTTPError as e_x:
        print("I couldn't find hd image"+str(e_x)) 
        return str("http://i.ytimg.com/vi/"+unique_id+"/hqdefault.jpg") 

class video_info(models.Model):
    def setup(self, ytd_dict):
        self.title          = ytd_dict.get('title')
        self.unique_id      = ytd_dict.get('id')
        self.duration       = ytd_dict.get('duration')
        self.uploader       = ytd_dict.get('uploader')
        self.view_count     = ytd_dict.get('view_count')
        self.img_url       = get_img(self.unique_id)
        #self.title_url      = quote( self.title, safe='')
        self.average_rating = float( ytd_dict.get('average_rating'))
        #print self.average_rating
        self.average_rating = round(self.average_rating, 3)        

    title           = models.CharField( max_length = 200,)
    unique_id       = models.CharField( max_length = 20,)
    duration        = models.IntegerField()
    img_url         = models.CharField( max_length = 60,)
    uploader        = models.CharField( max_length = 60,)
    view_count      = models.BigIntegerField()
    up_date         = models.DateTimeField(default = datetime.now, blank=True)
    counts          = models.IntegerField( default = 1)
    average_rating  = models.FloatField()
    num             = models.IntegerField(default = 0)
    def get_absolute_url(self):
        #Returns the url to access a particular book instance.
        return reverse('link-detail', args=[self.unique_id])
      # Metadata
    class Meta:
        ordering = ["-counts","-up_date",]

class number():
    num=0
    active=False