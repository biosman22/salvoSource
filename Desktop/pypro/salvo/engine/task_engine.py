
import os , math, requests, json

from  urllib.request import urlopen
from urllib.error import HTTPError


BASE_DIR =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWN_DIR =  os.path.join(BASE_DIR, "files")


def gettin_ready(url, title, format_id, ext):
    '''getting ready for the worker'''
    response = requests.get(url, stream = True)
    # Total size in bytes.
    total_size = int(response.headers.get('content-length', 0))
    #print("size is "+ str(total_size))
    max_allowed = 4*10**8
    print(max_allowed)
    #self.update_state(state='FAILURE', meta={'exc': "crap yo just crap"})
    if total_size >= max_allowed:
        return "failed"
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
        return 1
    else:
        return response

