# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from urllib.request import urlopen
from bs4 import BeautifulSoup

class playlist_video(object):
    def __init__(self, i, title, image, time, up ):
        self.title     =title
        self.img       = image
        self.timestamp =time
        self.uploader  =up
        self.ytd_id    = self.get_ytd_id(self.img)
        
        self.the_id    =i
    
    def get_ytd_id(self, img_url):
        id_index_start= img_url.find(u"/vi/")+4
        id_index_end= img_url.find(u"/hqdefault")

        ytd_id = img_url[ id_index_start : id_index_end ]
         
        return ytd_id
    
    
class Prase_yo(object):

    def __init__(self, list_url):

        self.playlist_video_list =[]
        r  = urlopen(list_url)
        soup = BeautifulSoup(r, "html.parser")
        #print 'lolololololl soup'
        [s.extract() for s in soup.body('script')]
        
        tag_list = soup.body.find("div","pl-video-list")
        if not tag_list:
            return     
           
        
        tag_titles = tag_list.find_all("tr","pl-video yt-uix-tile ")
        tag_imgs = tag_list.find_all("span", "yt-thumb-clip")

        tag_times = tag_list.find_all('div','timestamp')
        tag_uploaders = tag_list.find_all("a", " yt-uix-sessionlink spf-link ") 
        ##print soup.prettify()

       
        #print len(tag_imgs)
        #print len(tag_titles)
        #print len(tag_times)
        #print len(tag_uploaders)
        have_to_be_modified =[]
        for n in range(0, len(tag_imgs),1):
            if "no_thumbnail" in tag_imgs[n].img['data-thumb'] :
                have_to_be_modified.append(n)
                ##print "n "+str(n)
        have_to_be_modified = sorted(have_to_be_modified, reverse=True)
        for target_list in have_to_be_modified:
            ##print target_list
            del tag_titles[target_list]
            del tag_imgs[target_list]
        #print "modified"
        #print len(tag_imgs)
        #print len(tag_titles)
            
        if len(tag_imgs)== len(tag_titles) == len(tag_times)==len(tag_uploaders):
            for i in range( 0, len(tag_titles)):
                ##print tag_imgs[i].img['data-thumb']
                ##print tag_titles[i]['data-title']
                ##print tag_times[i].string
                ##print tag_uploaders[i].string
                a_pref = playlist_video(i,
                    tag_titles[i]['data-title'],
                    tag_imgs[i].img['data-thumb'],
                    tag_times[i].string,
                    tag_uploaders[i].string
                    )
                ##print a_pref.img
                self.playlist_video_list.append(a_pref)
            #print len( self.playlist_video_list) 


#soup =     BeautifulSoup("<html>data</html>")


