
#encoding:utf-8
from Spildertop import Spildertop
import threading,json
import time
import requests,re
def runGo(url,classid):
    print(Spildertop(url).runSpilder(classid))
    # Spildertop(url)

def getFile(url):
    with open(url) as f:

        # json_str=json.dumps(f.read())
        data_str=json.loads(f.read())
        return  data_str


# def return_stat():
#     try:
#
#         r=requests.get("http://baidutop.usegoods.com/996.html")
#         if r.status_code:
#             print()
#             return re.findall('<title>(.*?)</title>',r.text,re.S)[0];
#
#     except Exception:
#         return "404"
def main():

    # "'topmsg.json'"
    # myThread("实时热点", "http://top.baidu.com/buzz?b=1&c=513").start()
    # # runGo(" http://top.baidu.com/buzz?b=42&c=513")
    idjson=getFile("id.json")
    topjson=getFile("topmsg.json")
    # print(idjson)
    start=int(time.time())
    for i in topjson:
        try:
            # time.sleep(10)
            runGo(topjson.get(i),idjson.get(i))
            # myThread(i,topjson.get(i),idjson.get(i)).start()
        except requests.exceptions.ConnectionError:
            print("**********************")
            # myThread.join()
            # name.join
            # # thread1.start()
            # # thread2=myThread(2," 线程B",'http://top.baidu.com/buzz?b=341&c=513')
            # # thread2.start()
            # thread1.join()
            # thread2.join()
            # thread1.start()
    end = int(time.time())

    print(end-start)


if __name__ == '__main__':
    try:
        print("请稍等。。。。。。。。。。")
        main()

    except Exception:
        print("出现了错误，网络连接失败！请稍后再试")
