# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from datetime import datetime
import os, requests, math, json

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import template
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from  urllib.request import urlopen
from urllib.error import HTTPError


from .forms import url_form
from .engine import info_dicty, lol, getlink
from .models import  number, video_info, get_img, downloaded
from .prase_playlist import Prase_yo
from .tasks import download
# Create your views here.


BASE_DIR =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_ALLOWED = 4*10**8
##print BASE_DIR
 
sitemap_ = os.path.join( os.path.join( os.path.join(BASE_DIR,"engine"),"templates"),"sitemap.xml") 
##print sitemap_
# Create your views here.


register = template.Library()
#server="http://192.168.1.22:8000/engine/"
server="http://salvo.herokuapp.com/engine/"
#just

@csrf_exempt
def get_the_file(request):
    '''
    lol = json.dumps(request.POST)
    data = json.loads(lol)
    a_resut_id = data['result_id']
    '''
    a_resut_id  = request.POST.get('target_elem')
    a_record         = downloaded.objects.get(task_id = a_resut_id )
    with open(a_record.file_name,'rb') as target:
        return HttpResponse(target, a_record.content_type)


@csrf_exempt 
def download_and_return(request):
    print(request.POST)
    lolo = json.dumps(request.POST)
    data = json.loads(lolo)
    total_size =0

    with requests.get(data['url'], stream = True) as response:
    # Total size in bytes.
        total_size = int(response.headers.get('content-length', 0))
    #print("size is "+ str(total_size))
    max_allowed = 4*10**8
    print(max_allowed)
    #self.update_state(state='FAILURE', meta={'exc': "crap yo just crap"})
    if total_size >= max_allowed:
        return HttpResponse("<p style='color:red;'> sorry the file is too large !! </p>")
    else:
        result = download.delay(
        data['url'],
        data['title'],
        data['unique_id'],
        data['format_id'],
        data['ext']
         )

    print(data['title'])
    print(data['unique_id'])
    print(data['url'])
    print(data['format_id'])
    print(data['ext'])
    #print(result.id)
    return render(request, 'simple_test.html',
        context={'task_id': result.task_id,
            'progress_id':data['unique_id']+"progress"+data['format_id'],
            'bar_message_id': data['unique_id'] + "message" + data['format_id'],
            'back_server':server+ "ds_file",
            'server':server
            })
    #with open(reso.path,'wb') as handle:
        #return HttpResponse(handle, content_type=reso.content_type)
    '''
    response = requests.get(a_url,stream = True)
    # Total size in bytes.
    total_size = int(response.headers.get('content-length', 0)); 
    block_size = 128
    wrote = 0 
    with open('audioplayback'+total_size+'.'+str(new_link.ext),'wb') as handle:
        for data in tqdm(response.iter_content(block_size), total=math.ceil(total_size//block_size) , unit='MB', unit_scale=True):
            wrote = wrote  + len(data)
            handle.write(data)
    '''
    
def update_db( a_uniq):
    try:
        a_record         = video_info.objects.get(unique_id = a_uniq)
        a_record.counts  = a_record.counts+1
        a_record.up_date = datetime.now()
        a_record.save()
        return 1
    except ObjectDoesNotExist:           
        return 0

def top5(request):
    #print 'playlist fall back'
    return render(request,'ajax_top5.html',context={ "top":get_top5(),},)
    
def AwesomeSitemap(request):
    all_objects = video_info.objects.order_by('id').all()
    return render(request,'sitemap.xml',context={ "all":all_objects,},content_type='application/xhtml+xml')

def frame(request):
    #global len_all, last
    
    vid_id    = request.GET.get('v', "1")
    vid       = "https://www.youtube.com/watch?v="+ vid_id
    info_dict = info_dicty(vid)
    
    if  not isinstance(info_dict, str): 
        try:       
            new_lol = lol(info_dict)
            a_record = None
            new_video_info = None
            try:
                a_record         = video_info.objects.get(unique_id = vid_id)
                a_record.counts  = a_record.counts+1
                a_record.up_date = datetime.now()
                a_record.save()
            except ObjectDoesNotExist:        

                new_video_info = video_info()
                new_video_info.setup(info_dict)
                print(new_video_info.title)
                print(new_video_info.unique_id)
                print(new_video_info.img_url)
                print(new_video_info.uploader)
                print(new_video_info.duration)
                print(new_video_info.view_count)
                print(new_video_info.up_date)
                print(new_video_info.average_rating)
                 
                new_video_info.save()

            if a_record:
                info = a_record
            else:
                info = new_video_info

            return render(
                    request,'ajax_lol.html',
                    context={
                        "video" :info,
                        'ads'   :new_lol.my_audios,
                        'vds'   :new_lol.my_videos, 
                        'nads'  :new_lol.no_audios,
                        'webm'  :new_lol.webm,
                        'protected': new_lol.protected,
                        'back_server':server+"ds_file"
                        },)
        except Exception as e_x:
            print(e_x)
            return HttpResponse("<h1 class='text-primary'>sorry something gone worg</h1>")
    else:
        ##print 'stupid url'
        return HttpResponse( info_dict)
                
def play_list(request):

    playlist_link =  "https://www.youtube.com/playlist?list=" +request.GET.get('list', "1")
    #print "the link from views  "+playlist_link
    playlist_videos = Prase_yo(playlist_link).playlist_video_list
    if len (playlist_videos) > 0:
        return render(request,'ajax_playlist.html',context={ "list":playlist_videos,},)
    else:
       tt= top5(request)
       return tt

def test(request):
    #a_url = "https://en.savefrom.net/img/articles/youtube_com/ss_ru_1.png"
    add(39483039,2092309)
    a_url = "https://r1---sn-4g5ednek.googlevideo.com/videoplayback?keepalive=yes&expire=1524316232&lmt=1518286388922858&id=o-AKl6hBwi6A1-2nSR9tTPOZr5orp5CFgJopiQsbJ-4EBx&c=WEB&ipbits=0&clen=1821557&ip=54.216.239.24&dur=300.401&fvip=1&gir=yes&sparams=clen,dur,ei,expire,gir,id,initcwndbps,ip,ipbits,itag,keepalive,lmt,mime,mip,mm,mn,ms,mv,pl,requiressl,source&itag=249&ei=6OPaWqCJFNrRgAfCnbw4&key=cms1&pl=18&mime=audio%2Fwebm&requiressl=yes&source=youtube&signature=43A217247B5A5A0420B5642026174E7E0E86B790.4CC4B7FAF5E29BF6304B4C414C7B142D93D7528E&ratebypass=yes&redirect_counter=1&cm2rm=sn-q0ck76&req_id=60734b0d4c5ba3ee&cms_redirect=yes&mip=197.39.110.194&mm=34&mn=sn-4g5ednek&ms=ltu&mt=1524294805&mv=m"
    response = requests.get(a_url,stream = True)
    # Total size in bytes.
    total_size = int(response.headers.get('content-length', 0)); 
    #return render(request,'test.html')
    return HttpResponse(response.content ,content_type= response.headers['Content-Type'])


import json
from celery.result import AsyncResult


def progress_view(request):
    result = download.delay("https://r3---sn-uxaxjvhxbt2u-xhtl.googlevideo.com/videoplayback?clen=3490105&requiressl=yes&dur=219.707&pl=18&ip=54.78.12.182&lmt=1512108280362493&keepalive=yes&ei=PhDdWojgJMu0gQe4mI_gCQ&source=youtube&id=o-AEX4LZ6CJ4lcI2-yDbrFz9KF2Iog0pewP82Ej1cyNp36&key=cms1&gir=yes&expire=1524458654&sparams=clen,dur,ei,expire,gir,id,ip,ipbits,ipbypass,itag,keepalive,lmt,mime,mip,mm,mn,ms,mv,pl,requiressl,source&itag=140&fvip=3&ipbits=0&mime=audio%2Fmp4&c=WEB&signature=1727F267365D0A70ADE49D43EE37F22EEDE10F7D.3D96EFEF8756643109D2A32B1BA5C2BF2626ABFE&ratebypass=yes&redirect_counter=1&rm=sn-aigesr7s&req_id=3beee0642f04a3ee&cms_redirect=yes&ipbypass=yes&mip=197.39.110.194&mm=31&mn=sn-uxaxjvhxbt2u-xhtl&ms=au&mt=1524436912&mv=m",".m4a")
    return render(request, 'simple_test.html', context={'task_id': result.task_id})

class index(View):
    global server  
    
    def __init__(self):
        self.playlist_bool = False
        self.playlist_id = ""
        self.active_h=True
        self. playlist_list = None
        self.video_id = None
        self.first_id_index = None
        self.last_id_index  = None

    def filter_url(self, url_yo):
    
        self.first_id_index = url_yo.find("v=")+2
        self.last_id_index = url_yo.find("&")
        self.first_list_index = url_yo.find("list=")
        if self.last_id_index == -1:
            self.last_id_index = len(url_yo)
        #elif self.last_id_index < self.first_id_index:
            #print 'the fukin id is too get method gone wrong'

        if self.first_list_index > self.first_id_index:
            self.last_list_index = len(url_yo)
            self.playlist_id =url_yo[ self.first_list_index : self.last_list_index ]
            self.playlist_bool = True
            #print self.playlist_id
            #print self.playlist_bool
        elif self.first_list_index == -1:
            self.playlist_bool = False

        self.video_id = url_yo[self.first_id_index:self.last_id_index]

    def filter_url_be(self, url_yo):
    
        self.first_id_index = url_yo.find("youtu.be/")+9
        self.last_id_index = url_yo.find("&")
        self.first_list_index = url_yo.find("list=")
        if self.last_id_index == -1:
            self.last_id_index = len(url_yo)
        elif self.last_id_index < self.first_id_index:
            print('the fukin id is too get method gone wrong')

        if self.first_list_index > self.first_id_index:
            self.last_list_index = len(url_yo)
            self.playlist_id =url_yo[ self.first_list_index : self.last_list_index ]
            self.playlist_bool = True
            #print self.playlist_id
            #print self.playlist_bool
        elif self.first_list_index == -1:
            self.playlist_bool = False

        self.video_id = url_yo[self.first_id_index:self.last_id_index]

    def get(self, request):
        # Code block for GET request
        form = url_form(request.POST)
        return render(request, 'form.html', {"active_h":self.active_h,'form': form,'server':server,'first':get_first(),'recent':get_recent()})

    
    def post(self, request):
        # Code block for POST request
        form = url_form(request.POST)
        # create a form instance and populate it with data from the request:
        # check whether it's valid:
        ##print "Is it valid ?  yo "+str (form.is_valid())
        
        if form.is_valid():
            
            self.active_h=False
            url = str(form.cleaned_data['your_name'])

            if "watch?"in url:
                self.filter_url(url)
                #print self.playlist_bool
                
                # create filter for the template------------------------------------
                
                if self.playlist_bool:
                    #print self.playlist_bool
                    top5 = None
                else:
                    top5 = get_top5()
                

           # return HttpResponse(content, content_type='application/html',)
                return render(
                request,'lol.html',
                context={
                    "playlist"  :self.playlist_bool, 
                    "list_link" :self.playlist_id,
                    "active_h"  :self.active_h,
                    'first'     :get_first(),
                    'url_id'    :self.video_id,
                    'server'    :server,
                    'top'       :top5,
                    'recent'    :get_recent(),
                    },)
            elif "update_sitemap" in url:
                update_sitemap()
                return HttpResponse("updated lol "+ str( datetime.now()))
            elif 'youtu.be/' in url:
                self.filter_url_be(url)

                if self.playlist_bool:
                    #print self.playlist_bool
                    top5 = None
                else:
                    top5 = get_top5()
                return render(
                request,'lol.html',
                context={
                    "playlist"  :self.playlist_bool, 
                    "list_link" :self.playlist_id,
                    "active_h"  :self.active_h,
                    'first'     :get_first(),
                    'recent'    :get_recent(),
                    'url_id'    :self.video_id,
                    'server'    :server,
                    'top'       :top5,
                    },)
            else:
                return render(request, 'form.html', {"active_h":self.active_h,'form': form,'server':server,'first':get_first(),'recent'    :get_recent(),})

        
        else:
            pass
            '''all_videos_urls = request.POST.getlist('video-list')
            #print all_videos_urls
            if (all_videos_urls!= None):
    
                #print self.playlist_bool
                info_dict = info_dicty(all_videos_urls[0])
                
                new_video_info = video_info(info_dict)
                new_lol = lol(info_dict)
                for lin in all_videos_urls:
                    #print lin
                return render(
                request,'lol.html',
                context={
                    "pic":new_video_info.img_url,
                    "playlist":self.playlist_bool, 
                    "list":self.playlist_list,
                    "active_h":self.active_h,
                    'first':get_first,
                    'ads':new_lol.my_audios, 
                    'vds':new_lol.my_videos, 
                    'nads':new_lol.no_audios,
                    'tit':new_video_info.title,
                    'server':server,
                    'top':None,},)
                '''

#def index_old(request):
   # if first_obj != None:
   
sitemap_top = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n "
                +"<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"> \n"
                +" <url>\n<loc>http://salvo.herokuapp.com/engine</loc> \n "
                +"<lastmod>2017-12-25</lastmod> \n "
                +"<changefreq>never</changefreq> \n" 
                +"<priority>1.0</priority> \n"
                +"</url>\n")
def update_sitemap():
    open(sitemap_, 'w').close()
    put_a_sitemap = open(sitemap_,"r+")
    ##print put_a_sitemap.read()
    #lines = put_a_sitemap.readlines()
    #lines = lines[:-1]
    content=sitemap_top
    vid_list = video_info.objects.order_by('id').all()
    for vi in vid_list:
        content += ("<url>\n<loc>http://salvo.herokuapp.com/engine/t/"+vi.unique_id+
        "</loc> \n <lastmod>"+str(vi.up_date.date()) +
        "</lastmod> \n <changefreq>never</changefreq> \n <priority>0.5</priority> \n</url>\n")

    content+="</urlset>"
    put_a_sitemap.write(content)
    put_a_sitemap.close()

def top(request , stub):

    active_t=True
    #first_obj = video_info.objects.order_by("-counts").first()
 #--------------------------------------
    #get values from http request
    #============================

    #page = request.GET.get('page', '1')
    #page = int(page)
    try:
        #print "stub"+stub

        vid_info =  video_info.objects.get(unique_id__exact=stub)
        
        if vid_info.unique_id == get_recent().unique_id:
            the_url= server+"more?recent=1&n="
        else:
            the_url=server+"more?n="

        #print "counts is "+ str(vid_info.counts)
        ##print vid_info.title
        print(vid_info.img_url)
    except ObjectDoesNotExist:
        vid_info = None
    if  vid_info!= None:
        if "hqdefault.jpg" in vid_info.img_url:
            
            vid_info.img_url= get_img(vid_info.unique_id)
            vid_info.save()
        vid_info.num = video_info.objects.filter( counts__gt = vid_info.counts ).count()+1 +video_info.objects.filter( counts__exact = vid_info.counts, up_date__gt=vid_info.up_date).count()

        if vid_info.num != 1:
            active_t = False

    #for vi in vid_list:
        #vi.img_url = "http://i.ytimg.com/vi/"+vi.unique_id+"/hqdefault.jpg"
        #vi.save()
        ##print "__________________________________________________"
        ##content += "<url>\n<loc>"+ vi.web_url +"</loc> \n <lastmod>"+ str(vi.up_date) +"</lastmod> \n <changefreq>never</changefreq> \n <priority>0.5</priority> \n</url>\n"
        #vid_stupid =  video_info.objects.filter(unique_id__exact=vi.unique_id)
        
        #if len(vid_stupid) >1:
       #     #print "vid_s len=  "+str(len(vid_stupid))
            #for v in range(1,len(vid_stupid),1) :
         #       #print "deleted "+ vid_stupid[v].title
                #vid_stupid[v].delete()
        #vi.img_url = set_high_img(vi.img_url)
        #vi.save()
        #if vi.title_url == 'empty':
        #vi.title_url = quote( vi.title, safe="" )
        #if vi.average_rating>50 :
          #  vi.average_rating/=20
           # vi.save()
            
        #elif "Qur'an" in vi.title:
         #   vi.delete()
        #vi.delete()

        ##print vi.counts
        ##print vi.id
    #put_a_sitemap.write(content)
    #put_a_sitemap.close()
    print(vid_info.duration)
    all_is = str(video_info.objects.all().count())
    print('all_is is '+str(all_is) )
    return render(request, 'top.html', 
        {
            'active_t' :active_t,
            'server':server,
            'no1':vid_info,
            'first':get_first(),
            'recent': get_recent(),
            'all':all_is,
            'the_url':the_url,
        })

def more(request):

    global server

    recent = request.GET.get('recent', '0')
    recent = int(recent)
    n = request.GET.get('n', '0')
    n = int(n)
    vid_list = None
    if recent == 1:
        vid_list = video_info.objects.order_by('-up_date')[n:n+9]
    else:
        vid_list = video_info.objects.all()[n:n+9]
    
    #hide_button = 0
   
   
    #if all_is <= n+9:
    #    hide_button = 1
    
    return render(request, 'ajax_top.html', 
        {   'server':server,
            'vids': vid_list,
     #       "hide_button":hide_button,
           
        })

    
def just_all_titles(request):
    all_videos = video_info.objects.all()
    titles =""
    for element in all_videos:
        titles +=" <br> "+ str(element.id) +"&ensp; "+ element.title 
    return HttpResponse(titles)

def get_first():
    first_obj = video_info.objects.first()
    return first_obj
    #return None


def get_recent():
    first_obj = video_info.objects.order_by('-up_date').first()
    return first_obj
    #return None

def about(request):
    top5 = get_top5()
    return render(request, 'about.html',{'first':get_first(),'server':server,'top':top5,'about_active':True})
def err400(request):
    top5 = get_top5()
    return render(request, '400.html',{'first':get_first(),'server':server,'top':top5})
def err403(request):
    top5 = get_top5()
    return render(request, '403.html',{'first':get_first(),'server':server,'top':top5})
def err404(request):
    top5 = get_top5()
    return render(request, '404.html',{'first':get_first(),'server':server,'top':top5})
def err500(request):
    top5 = get_top5()
    return render(request, '500.html',{'first':get_first(),'server':server,'top':top5})

def get_top5():
    Top_list = video_info.objects.all()[:5]

    for i in range(len(Top_list)):
        Top_list[i].num = i+1

    return Top_list
