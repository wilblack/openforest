import os
from datetime import datetime as dt
from pinax.apps.photos.models import Image
from django.contrib.auth.models import User
from threadedcomments.models import FreeThreadedComment
from features.models import Feature

class Droid():
    '''
    Class to handle a uploads from my Android.
    Set Droid.path to wherever the upload directory is.
           
    '''
    
    def __init__(self):
        self.path = '/home/wilblack/android/' # Directory to look for photos
        self.bn = 'uid_1_'      # file basename used torename file.
        self.file = None
        self.fname =""
        self.dest_path = '/home/wilblack/social/site_media/media/photologue/photos/'
        
    def ls(self):
        return os.listdir(self.path)
        
    def get_new(self):
        '''
        Get all unprocessed logs in self.path. 
        Returs a list of filnames
        '''
        import re
        listDir=self.ls()
        r=range(len(listDir))
        r.reverse()
        for i in r:
            if not re.search('\d\d.txt$',listDir[i]):listDir.pop(i)         
        return listDir              
    def ls2html(self):
       '''
       Returns an html select menu of the directory listing in self.path. 
           name=logFileName
       
       ''' 
       html = "<div>"
       html+= "<div>%s</div>" %(self.path)
       html +="<ol name='logFileName' class='selectable'>"
       for l in self.ls():
           verbose = l.replace('_',' ').replace('h', ' hour ')
           verbose = verbose.split('.')[0]
           html +="<li title='%s' class='ui-widget-content'>%s</li>" %(l,verbose)
       html +="</ol>"
       html +="</div>" 
       return html
   
   
    def _setp(self):
        '''
        Inserts a p in front of the dot to signify processed.
        '''
        l=self.fname.split('.')
        pName=l[0]+'p.'+l[1]
        os.rename(os.path.join(self.path,self.fname),os.path.join(self.path,pName))
    
    def load_pics(self):
        '''
        Grabs all unprocessed files with extensions .png or .jpg
        and loads them into photologue
        '''
        import shutil
        member = User.objects.get(username='wilblack') # Open forest member object
                
        newPhotos=[]        
        for l in self.ls():
            if os.path.splitext(l)[1] in ['.png','.jpg','.jpeg']:
                src_image=os.path.join(self.path,l)
                dest_image = os.path.join(self.dest_path,l)
                if os.path.exists(dest_image):
                    continue
                
                shutil.move(src_image,self.dest_path)
                newPhotos.append(l)
                img = Image(title=l, 
                            member=member, 
                            image="photologue/photos/"+l,
                            safetylevel=1,
                            )
                img.save()
        self.newPhotos=newPhotos
                
    def assign_project(self):
       ftc=FreeThreadedComment.objects.latest()
       if ftc.name=='Android':
           feature = Feature.objects.get(pk=ftc.object_id)
                      #photoList = json.loads(ftc.comment)
           for p in self.newPhotos:
               img = Image.objects.get(title=p)
               img.photoset.add(feature.photoset)
               img.save()
           
       
       
        

