#encoding:utf-8
import requests,re
from DB.UtilInSertDB import InsertDB;
from bs4 import BeautifulSoup
import json
import traceback
class Spildertop:
    def __init__(self,url):
        self.url=url
        self.__hearders = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}



    def getFile(self,url):
        with open(url) as f:
            # json_str=json.dumps(f.read())
            data_str = json.loads(f.read())
            return data_str


    # 得到要抓取的内容
    def __getFile(self):
        with open('topmsg.json') as f:

            # json_str=json.dumps(f.read())
            data_str=json.loads(f.read())
            return  data_str


    # 获取top50的链接
    def __getUrl(self,url):

        r = requests.get(url,headers=self.__hearders)
        r.encoding='gb2312'
        # print(r.text)
        content=r.text
        # print(content)
        UrlTitle=re.findall('<a class="list-title" target="_blank" href="(.*?)" href_top=".*?">(.*?)</a>',content,re.S)
        # print(UrlTitle)
        return  UrlTitle


    #获取新闻内容
    def __getContent(self,url):
        flag=(re.search('https://baijiahao.baidu.com/s\?id=\d+&wfr=spider&for=pc',url))
        if(flag):

            json = {}
            r = requests.get(url,headers=self.__hearders)
            r.encoding = 'utf-8'
            content = r.text
            # html = etree.HTML(content)
            Title = re.findall('<title>(.*?)</title>', content, re.S)
            auth = re.findall(
                '<div class="author-txt"><p class="author-name">(.*?)</p><div class="article-source article-source-bjh"><span class="date">(.*?)</span><span class="time">(.*?)</span></div></div>',
                content, re.S)
            if (auth != []):
                json['auth'] = auth[0][0];
                json['time'] = auth[0][1] + " " + auth[0][2];

            soup_string = BeautifulSoup(content, "html.parser")

            htmldivcontent = soup_string.select('.article-content')[0]

            json['content'] = htmldivcontent

            json['title']=Title[0]
            return  json


    #获取百度搜索链接
    def __getbaiduUrl(self,url):
        baijiahaoUrl=[]

        r=requests.get(url,headers=self.__hearders)
        r.encoding = 'utf-8'

        content = r.text

        urlHTML=re.findall('<div class="c-row">(.*?)</div>',content,re.S)
        for i in urlHTML:

            url=re.findall('href="(.*?)"',i,re.S)
            if(len(url)==1):
                baijiahaoUrl.append(url[0])

        return  baijiahaoUrl

    #获取真实的链接
    def __baijiahaoUrl(self,url):
        hearders = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'
        }

        r = requests.get(url,headers=self.__hearders, allow_redirects=False)
        r.encoding = 'utf-8'
        return r.headers['Location']

    def runSpilder(self,classID):
        try:
            print("开始爬取************************************")
            for top in self.__getUrl(self.url):
                if(len(top)==2):
                    # print(top[0])
                    getbaidu=self.__getbaiduUrl(top[0])
                    if (getbaidu!=[]):

                        if(self.__baijiahaoUrl(getbaidu[0])!=[]):
                            print(self.__baijiahaoUrl(getbaidu[0]))
                            dist_content=self.__getContent(self.__baijiahaoUrl(getbaidu[0]))
                            print(dist_content)
                            if(dist_content!=None):
                                print(dist_content)
                                #调用数据库的插入

                                self.Save_db(classID,dist_content.get('title'),dist_content.get('title'),dist_content.get('auth'),dist_content.get('auth'),dist_content.get('content'))
                        else:



                            print("错误**"+top)
        except requests.exceptions.ConnectionError:
                     print("**********************")
    def Save_db(self,classID,title,desc,author,befrom,content):
        try:
            dbmessage=self.getFile("DB/manger.json")
            # print(dbmessage.get('user'))
            x = InsertDB(dbmessage.get('user'),dbmessage.get('port'),dbmessage.get('host'),dbmessage.get('password'),dbmessage.get('database'))

            #x.find_titile(classID,title)
            if(x.find_titile(classID,title)==False):

                x.insert_news_index(classID)
                x.insert_news(classID, title, desc)
                x.insert_news_data_1(x.getID(), classID, author, befrom, content)
                x.phome_enewsclass(classID)
                x.rm_id()

            else:
                print("重复！")
            x.commit()
            x.close()
        except Exception :
            print("erro")
            x.rolback()

