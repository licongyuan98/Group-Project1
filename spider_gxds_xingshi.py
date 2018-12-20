import urllib.request
import re
import os
from bs4 import BeautifulSoup
import requests
#要爬取的网页url
url="http://www.guoxuedashi.com/xingshi/"

#创建若干列表 存储爬取内容
#为了写入文件提供方便
name=[]
name_urllist=[]
img_urllist=[]
explain=[]
l=""

#定义get_page(url)函数
#作用：以url为参数可获取网页所有内容
'''
def get_page(url):
    req=urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12918.400')
    response=urllib.request.urlopen(url)
    html=response.read().decode('utf-8')
    return html
'''
def get_page(url):
    try:
        html = requests.get(url, timeout=30)
        html.raise_for_status()
        html.encoding = html.apparent_encoding
        return html.text
    except:
        return ""

content=get_page(url) #获取网页所有内容
content=content[6401:35000]  #规定爬取范围
soup=BeautifulSoup(content,"html.parser")

#爬取内容部分
for string in soup.strings: #爬取所有字符串并添加到姓名列表
    name.append(repr(string))
    print("姓名列表爬取成功")
    
for a in soup.find_all('a', href=True): #爬取所有链接添加到姓名链接的列表
    name_urllist.append("http://www.guoxuedashi.com"+a['href'])#同时这些url就是要爬取的二级页面
    print("姓名url列表爬取成功")

#爬取二级页面(前10个)
for each in name_urllist[0:10]:
    l=""
    m=get_page(each)  #获取二级页面内容 
    m1=m[6537:6645]   #含图片的代码部分
    m2=m[6645:]       #姓氏详解的代码部分
    bs1=BeautifulSoup(m1,"html.parser")  #图片部分
    bs2=BeautifulSoup(m2,"html.parser")  #姓氏详解
    for a in bs1.find_all('img', src=True):  #获取图片url
       img_urllist.append("http://www.guoxuedashi.com"+a['src'])
       print("图片url列表爬取成功")

    for x in bs2.find_all('p'): #获取内容部分
        for str in x.descendants:
            if type(str) == type(x):
                None
            else:
                l=l+str.string
    q=l.replace(" ","")  #处理文字内容
    r=q.replace("\n", "")
    v=r.replace("\r", "")
    explain.append(v)   #将姓氏详解加入列表

    print("姓氏解释列表爬取成功")

mark=len(explain)  #统计姓氏数量 方便循环中计数
s=0  
#创建文件
f=open('姓氏数据.txt','a+',encoding='utf-8')
#写入文件
#依次写入 姓氏/姓氏url/图片url/姓氏详解
while(s<=mark-1):
    f.write(name[s]+"\n")
    f.write(name_urllist[s]+"\n")
    f.write(img_urllist[s]+"\n")
    f.write(explain[s].encode('UTF-8', 'ignore').decode('UTF-8')+"\n")
    print(s)
    s=s+1
    
        
f.close()
       
    

