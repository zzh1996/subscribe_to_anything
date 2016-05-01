from app.repeat import *
from app.download import *
from app.mail import *
import sys
import time
from termcolor import colored
import difflib

def now():
    return time.asctime(time.localtime(time.time()))

def gendiff(oldtext,newtext,method):
    d=difflib.Differ()
    diff=d.compare(oldtext.splitlines(True),newtext.splitlines(True))
    if method=='all':
        return newtext
    elif method=='diff':
        return '\n'.join([line for line in diff if line[0] in ['+','-']])
    elif method=='new':
        return '\n'.join([line for line in diff if line[0]=='+'])

def processtask(page,data):
    print(now()+' [Processing task] ',page.name,file=sys.stderr)
    try:
        text=download(page.url,page.ua,page.referer,page.cookie,page.method,page.postdata)
    except Exception as e:
        print(page.id,page.name,type(e).__name__,file=sys.stderr)
        return
    if not data:
        data.append(text)
    else:
        if data[0]!=text: #page changed!
            if page.watch_type=='change':
                notify=gendiff(data[0],text,page.notify_content)
                send_mail(
                    page.name+' - subscribe to anything',
                    notify,
                    page.email()
                )
            elif page.watch_type=='keyword':
                pass
            data[0]=text


class Daemon():
    def __init__(self):
        self.tasks=[]

    def addtask(self,page):
        data=[]
        processtask(page,data)
        #task=page,Repeater(page.freq*60,processtask,page,data)
        task=page,Repeater(page.freq,processtask,page,data)
        task[1].start()
        self.tasks.append(task)
        print(colored('Add task','red'),page.name,file=sys.stderr)
        print('Task Count:',len(self.tasks),file=sys.stderr)

    def deletetask(self,pageid):
        for task in self.tasks:
            if task[0].id==pageid:
                task[1].stop()
                print(colored('Delete task','red'),task[0].name,file=sys.stderr)
                self.tasks.remove(task)
        print('Task Count:',len(self.tasks),file=sys.stderr)

    def loadall(self):
        from app import models
        for page in models.Page.all():
            self.addtask(page)


