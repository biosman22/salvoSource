
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re, requests
from .youtube_dl import YoutubeDL
from .youtube_dl.utils  import ExtractorError, YoutubeDLError

'''import ffmpeg

ydl_options = {format :'[height <? 720]',}
ydl = YoutubeDL(ydl_options)
video_title = ''
id = ''
file_name = ''
def get_it(video_url):
    global id , video_title , file_name
    #ydl.download([video_url])
    info_dict = ydl.extract_info(video_url)
    video_title = info_dict.get('title', None)
    #print video_title
    id = info_dict.get('id', None)
    #print id
    file_name = video_title + '-' + id + '.mp4'
    #print 'file name is  = '+ file_name

overlay_file = ffmpeg.input('overlay.png')

import os
import subprocess
BASE_DIR =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(BASE_DIR,'data')


def convert():
    global video_title , file_name , overlay_file , BASE_DIR, data_path
    #print BASE_DIR
    file_name = os.path.join(BASE_DIR , file_name)
    file_obtained = video_title + '.mp4'
    final = os.path.join(data_path , file_obtained)
    #print file_name
    stream = ffmpeg.input(file_name,shell=True)
    stream = ffmpeg.overlay(stream , overlay_file)
    stream = ffmpeg.drawbox(stream , 50, 50, 120, 120, color='red', thickness=5)
    stream = ffmpeg.output(stream,final,shell=True)
    ffmpeg.run(stream)

'''

ydl_opts = {'format':'all',}#'listsubtitles':True}
mp4_videos_id = [
    133,
    134,
    135,
    136,
    137,
    138,
    160,
    212,
    264,
    298,
    299,
    266
]
webm_videos_id = [
    167,
    168,
    169,
    170,
    218,
    219,
    278,
    242,
    243,
    244,
    245,
    246,
    247,
    248,
    271,
    272,
    302,
    303,
    308,
    313,
    315
]
server_back = "http://192.168.1.22:7000/checker/"
#server_back = "http://salvoengine.herokuapp.com/checker/"

class A_link(object):
    def __init__(self, title, unique_id, formats_dict):
        self.url        = formats_dict.get("url")
        self.ext        = formats_dict.get("ext")
        self.title      = title
        self.format_id  = formats_dict.get("format_id")
        self.unique_id  = unique_id

def getlink(info_dict, format_id):
    title = info_dict.get('title')
    unique_id = info_dict.get('id')
    formats = info_dict.get('formats')
    ##print formats
    for di in formats:
        if di.get("format_id") == format_id :
            new_link = A_link( title, unique_id, di)
            return new_link
    return None
    
class no_audio(object):
    def __doc__(self):
        '''just for temlate'''
    def __init__(self, mp4, webm):
        self.mp4  = mp4
        self.webm = webm

def beautiful_size(size):
    i=0
    ss=[" KB"," MB"," GB"]
    while size >= 1024:
        size = size/1024.0
        i+=1
        size = round(size,2)
    return str(size)+ss[i-1]

class link_info_rocks(object):
    def __init__(self, formats_dict):
        self.url    = formats_dict.get("url")
        self.size   = formats_dict.get("filesize")
        self.format_id  = formats_dict.get("format_id")
        if self.size != None:
            self.size   = beautiful_size(self.size)
        
        self.ext    = formats_dict.get("ext")
        self.abr    = str(formats_dict.get('abr'))
        self.fps    = str(formats_dict.get('fps'))
        ##print "fps = "+str(self.fps)
        self.height = str(formats_dict.get('height'))
        self.width  = str(formats_dict.get('width'))
        if 'audio' in formats_dict.get('format_note'):
            self.type  = 0
        elif int(formats_dict.get('format_id')) in mp4_videos_id:
            self.type = 1
        elif int( formats_dict.get('format_id')) in webm_videos_id:
            self.type = 2
        else:
            response = requests.get(self.url,stream = True)
            # Total size in bytes.
            total_size = int(response.headers.get('content-length', 0))
            self.size = beautiful_size(total_size)
            self.type = 3

def info_dicty(video_url, playliststart = 1, playlistend = None):
    ydl_opts.update({'playliststart': playliststart, 'playlistend':playlistend})
    ydl = YoutubeDL(ydl_opts)
    #print ExtractorError
    try:
        info_dict = ydl.extract_info(video_url, download=False)
    except YoutubeDLError as identifier:
        info_dict = str(identifier)
        rStart =  info_dict.find("0m")
        if rStart !=-1:

            info_dict = "<h3>Sorry about that</h3> <br>"+ info_dict[rStart+3:]
        #print 'another catched yoyoyoyoyo'
        #print "the identifier"+str(identifier)
    return info_dict

from  urllib.request import urlopen
from urllib.error import HTTPError


class lol(object):
    """lolol"""
    def __init__(self, info_dict):
        self.webm = False
        self.my_audios=[]
        self.my_videos=[]
        self.no_audios = []
        self.my_only_videos_mp4=[]
        self.my_only_videos_webm=[]
        self.first_check = True
        self.protected = False
        self.getlinks(info_dict)
        
        

    def getlinks(self,info_dict):
        formats = info_dict.get('formats')
        ##print formats
        for di in formats:
            new_link = link_info_rocks(di)
            '''#print '----------------start-----------'
            ##print new_link.url

            #print new_link.height
            #print new_link.width
            #print new_link.ext
            #print new_link.size
            #print "abr"+new_link.abr
            #print"fps"+(new_link.fps)

            #print 'mp4 is ' +str(new_link.vid_mp4)
            #print 'webm is '+str(new_link.vid_webm)
            '''

            '''if self.first_check:
                print('check')
                response_ = requests.post(server_back, data={'url':new_link.url})

                if  response_.status_code== 200:
                    #urlopen(new_link.url)
                    print("awesome engine")
                else:
                    self.protected = True
                    print("I couldn't find the links (engine) ")
                    #a_url = "http://i.ytimg.com/vi/rWNKAXAAFmY/maxresdefault.jpg"
                self.first_check = False
            '''
            if new_link.type == 0:
                self.my_audios.append(new_link)
            elif new_link.type == 1:
                self.my_only_videos_mp4.append(new_link)
            elif new_link.type == 2:
                self.my_only_videos_webm.append(new_link)
            else :
                self.my_videos.append(new_link)
        #print "mp4 length"+str(len(self.my_only_videos_mp4))
        #print "webm length"+str(len(self.my_only_videos_webm))
        if(len(self.my_only_videos_mp4) == len(self.my_only_videos_webm) ):
            self.webm = True
            for target in range( 0, len (self.my_only_videos_mp4), 1):
                n_ad = no_audio(self.my_only_videos_mp4[target], self.my_only_videos_webm[target])
                self.no_audios.append(n_ad)
        elif len(self.my_only_videos_mp4) !=0 and len( self.my_only_videos_webm) ==0:
            for target in range( 0, len (self.my_only_videos_mp4), 1):
               n_ad = no_audio(self.my_only_videos_mp4[target],None)
               self.no_audios.append(n_ad)
            
