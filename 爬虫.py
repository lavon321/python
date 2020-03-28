import requests
import re
import threading
import os
def getContent(s,Chapter_title):
    reg='<h1>(.*)</h1>'
    head=re.findall(reg,s.text)
    head=str(head[0])
    reg2 = r'<div id="content" class="showtxt">(.*)小说族手机版阅读网址：m.xiaoshuozu8.com'
    content=re.findall(reg2,s.text)
    content=str(content)
    reg3=r'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(.*?)<br />'
    content=re.findall(reg3,content)
    with open('D:/{}/{}.txt'.format(Chapter_title,head),'w') as f:
        f.write(head+'\n\n\n')
        for x in content:
            x=x.replace('\\r','')
            f.write(x+'\n\n')
        print('{}  章节：{}  下载成功！'.format(Chapter_title,head))
def spider(n,baseurl,Chapter_title):
    os.mkdir('D:/'+Chapter_title)
    s=request(baseurl+str(n))
    re1='<dd><a href ="/shu/{}/(.*?)\\.html">'.format(str(n))
    a=re.findall(re1,s.text)
    min=int(a[0])
    max=int(a[0])
    for i in a:
        if(int(i)<min):
            min=int(i)
        if(int(i)>min):
            max=int(i)
    for j in range(min,max):
        Request=baseurl+str(n)+'/'+str(j)+'.html'
        Request=request(Request)
        getContent(Request,Chapter_title)
def preview(n,url,List):
    count=0
    reg='<h1>(.*)</h1>'
    c=request(url+str(n))
    Chapter_title=re.findall(reg,c.text)
    Chapter_title=str(Chapter_title[0])
    re1='<dd><a href ="/shu/{}/(.*?)\\.html">'.format(str(n))
    chapter=re.findall(re1,c.text)
    for i in chapter:
        count+=1
    print('小说名：'+Chapter_title)
    print('当前小说章节数：{}章节'.format(count))
    ch=input('是否加入下载？[y/n] \n')
    if(ch=='y'):
        t=threading.Thread(target=spider,args=(n,url,Chapter_title))
        List.append(t)
        # print(List)
def request(url):
    trytimes=6  
    count=0
    for i in range(trytimes):
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                return response
        except:
            count+=1
            print('请求超时，正在重试、、、')
            if(count==6):
                print('错误原因：网络状态不佳')
def main():
    n=46811
    threads=[]
    baseurl='https://www.xiaoshuozu8.com/shu/'
    preview(n,baseurl,threads)
    a=input('是否寻找其它小说？[y/n] \n')
    while a=='y':
        choose=input('请选择下一部或者上一部小说[next/pre]。\n或输入任意键退出选择，并开始下载\n')
        if(choose=='pre'):
            n-=1
            preview(n,baseurl,threads)
        elif(choose=='next'):
            n+=1
            preview(n,baseurl,threads)
        else:
            a='n'
            for i in threads:
                i.start()
main()
