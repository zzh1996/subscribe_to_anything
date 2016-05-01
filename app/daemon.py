from app.repeat import *
from app.models import *
from app.download import *
import sys
import time

def now():
    return time.asctime(time.localtime(time.time()))

def gendiff(oldtext,newtext,method):
    if method=='all':
        return newtext
    elif method=='diff':
        pass
    elif method=='new':
        pass

def processtask(page,data):
    print(now()+' [Processing task] ',page.name,file=sys.stderr)
    try:
        text=download(page.url,page.ua,page.referer,page.cookie,page.method,page.postdata)
        if not data:
            data.append(text)
        else:
            if data[0]!=text: #page changed!
                if page.watch_type=='change':
                    notify=gendiff(data[0],text,page.notify_content)
                    send_mail(
                        page.name+' - subscribe to anything',
                        notify,
                        page.user.email
                    )
                elif page.watch_type=='keyword':
                    pass
    except Exception as e:
        print(page.id,page.name,type(e).__name__,file=sys.stderr)


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
        print('tasks:',self.tasks,file=sys.stderr)

    def deletetask(self,page):
        for task in self.tasks:
            if task[0]==page:
                task[1].stop()
                self.tasks.remove(task)
        print('tasks:',self.tasks,file=sys.stderr)

    def loadall(self):
        for page in Page.all():
            self.addtask(page)


