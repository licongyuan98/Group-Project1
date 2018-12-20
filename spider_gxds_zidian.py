from bs4 import BeautifulSoup
import requests
import json
import re
#要爬取的网页url
url = "http://www.guoxuedashi.com/zidian/"

#定义get_page(url)函数
#作用：以url为参数可获取网页所有内容
def get_page(url):
    try:
        html = requests.get(url, timeout=30)
        html.raise_for_status()
        html.encoding = html.apparent_encoding
        return html.text
    except:
        return ""


content = get_page(url)  #获取网页所有内容
content = content[6400:43980]  # 规定网页要爬取的范围
soup = BeautifulSoup(content, "html.parser")

#以索引名称建立文件
#index_url = []

for a in soup.find_all('a', href=re.compile('/zidian')): #对一级页面url进行筛选并爬取
    file_name = a.get_text() #得到索引名称
    path = file_name +'.json' #json格式文件存储
    index_url = "http://www.guoxuedashi.com" + a['href'] #得到二级页面url
    content = get_page(index_url)
    soup = BeautifulSoup(content,"html.parser")
    hanzi = soup.find(name='table', attrs={"class": "table2"}) 
    hanzi_url = []
    for a in hanzi.find_all('a', href=True):
        hanzi_url.append("http://www.guoxuedashi.com" + a['href']) #得到三级页面url


#三级页面爬取开始
    success = []   #最后写入json文件的字典
    for each in hanzi_url:
        content = get_page(each)
        soup = BeautifulSoup(content,"html.parser")
        exp = soup.find(name='div', attrs={"class": "info_txt2 clearfix"})

        #源网页的网页编写并不规范，我们需要对代码进行一些处理
        #将影响我们爬取的代码删除，
        delete = exp.find_all('p')[1]
        div_name = delete.style
        div_name.decompose()
        #将标签统一成table，方便下一步的筛选
        producer_entries = exp.p
        producer_entries.name = "table"
        #处理结束


        #正式开始处理网页内容
        h = soup.find(name='div',attrs={"class":"info_tree"})
        h1 = h.find_all('h1')[0] #找大标题
        
        if h1:
            word = h1.string   #取出文字
            explain = []       #创建一个字典存储解释


            entry1 = soup.find_all('h2')[0]
            entry_text1 = entry1.string  #键名1
            

            entry2 = soup.find_all('h2')[1]
            entry_text2 = entry2.string  #键名2
            

            entry3 = soup.find_all('h2')[2]
            entry_text3 = entry3.string  #键名3

            #值1
            exp_para1 = exp.find_all('table')[1]  
            exp_para_text1 = exp_para1.get_text()
            exp_para_text1 = exp_para_text1.replace("\n","").replace("\r","").replace("\t","")

            #值2
            exp_para2 = exp.find_all('table')[2]
            exp_para_text2 = exp_para2.get_text()
            exp_para_text2 = exp_para_text2.replace("\n", "").replace("\r","").replace("\t","")

            #值3
            exp_para3 = exp.find_all('table')[3]
            exp_para_text3 = exp_para3.get_text()
            exp_para_text3 = exp_para_text3.replace("\n", "").replace("\r","").replace("\t","")

            #创建列表存储下一页面的图片链接
            img_src = []
            for a in soup.find_all('a',href=re.compile('/kangxi')):
                img_index_url = "http://www.guoxuedashi.com" + a['href']
                content = get_page(img_index_url)
                soup = BeautifulSoup(content, "html.parser")
                for a in soup.find_all('img', src=re.compile('http://pic.')):
                    img_src.append(a['src'])



            #存入字典
            explain.append({entry_text1:exp_para_text1,entry_text2:exp_para_text2,entry_text3:exp_para_text3,"pic":img_src})
            success.append({'word':word,'content':explain})

            #写入文件
            with open(path,'w') as fp:
                json.dump(success, fp, ensure_ascii= False ,indent=4,separators=(',', ': '))
                print("loaded...")


    










