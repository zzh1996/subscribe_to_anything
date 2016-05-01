import requests,json
from bs4 import BeautifulSoup

def download(url,ua,referer,cookie,method,postdata):
    headers={'User-Agent':ua,'Referer':referer,'Cookie':cookie}
    if method=='POST':
        r=requests.post(url,headers=headers,data=json.loads(postdata),timeout=5)
    else:
        r=requests.get(url,headers=headers,timeout=5)
    soup=BeautifulSoup(r.content,"html5lib")
    for script in soup(["script", "style"]):
        script.extract()
    text=soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

