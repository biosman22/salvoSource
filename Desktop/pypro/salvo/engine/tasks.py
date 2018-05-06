# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from  urllib.request import urlopen
from urllib.error import HTTPError
from celery_progress.backend import ProgressRecorder

from datetime import datetime

import os , math, requests, json
from django.http import HttpResponse
from celery.exceptions import SoftTimeLimitExceeded

from .models import downloaded

BASE_DIR =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWN_DIR =  os.path.join(BASE_DIR, "files")



@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task(bind=True, soft_time_limit=600, default_retry_delay=30, max_retries=3,)
def download(self, url, title, Unique_Id, format_id, ext):
    progress_recorder = ProgressRecorder(self)
    #for i in range(0,40):
    #    progress_recorder.set_progress(i, 40)
    #return "lol"
    # Total size in bytes.
    response = requests.get(url, stream = True)
    # Total size in bytes.
    total_size = int(response.headers.get('content-length', 0))
    #print("size is "+ str(total_size))

    one_precent = total_size/100
    current_precent = 1
    block_size = 128
    wrote = 0
    file_name = title + "_" + format_id +'.'+str(ext)
    the_path = os.path.join( DOWN_DIR, file_name)
    #downloaded.objects.all().delete()
    #print("all is " +str(downloaded.objects.all()))
    if os.path.isfile(the_path):
        a_record         = downloaded.objects.get(file_name = the_path )
        a_record.up_date = datetime.now()
        a_record.task_id =  self.request.id
        print(a_record.file_name)
        print(a_record.content_type)
        print(a_record.up_date)
        print(a_record.task_id)
        a_record.save()
        #downloaded.objects.all().delete()
        #print("all is " +str(downloaded.objects.all()))

        return 'done'
    try:
        print(response.headers)
        response.headers['X-Sendfile'] = the_path
        response.headers['Content-Disposition'] = "attachment; filename='"+ file_name+"'"
        with open(the_path,'wb+') as handle:
            
            for data in response.iter_content(block_size): # tqdm(response.iter_content(block_size), total=math.ceil(total_size//block_size) , unit='MB', unit_scale=True):
                wrote += len(data)
                if wrote > one_precent* current_precent:
                    current_precent += 1
                    # tell the progress observer how many out of the total items we have processed
                    print("precent"+ str(current_precent))
                    progress_recorder.set_progress(current_precent-1, 100)
                handle.write(data)
                handle.flush()
            #return Reso(the_path, response.headers['Content-Type'])
        a_record =  downloaded()
        a_record.setup(the_path, response.headers['Content-Type'], datetime.now(), self.request.id, Unique_Id )
        print(a_record.file_name)
        print(a_record.content_type)
        print(a_record.up_date)
        print(a_record.task_id)
        a_record.save()
        return "done"
        
    except SoftTimeLimitExceeded:
        if os.path.isfile(the_path):
            os.remove(the_path)
        else :
            print('There was an error opening the file!')
        return 'failed'



