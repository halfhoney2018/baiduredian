#!/usr/bin/env python3
# -*- coding: utf-8 -*-

########## prepare ##########

# install mysql-connector-python:
# pip3 install mysql-connector-python --allow-external mysql-connector-python

import mysql.connector
import time,json
import datetime






class InsertDB():


    def __init__(self,user,port,host,password,database):
        # self.url=url
        self.user=user
        self.port=port
        self.host=host
        self.password=password
        self.database=database
        self.conn = mysql.connector.connect(user=self.user ,port=int(self.port),host=self.host,password=self.password,database=self.database)

        self.cursor = self.conn.cursor()
        self.i = datetime.datetime.now()
        self.nowintdate=int(time.time())


    def commit_sql(self,sql):
        # 创建user表:
        try:
            self.cursor.execute(sql)
            # 插入一行记录，注意MySQL的占位符是%s:
            # cursor.execute('insert into user (id, name) values (%s, %s)', ('1', 'Michael'))
            if(self.cursor.rowcount==1):
                print("Insert Success!")
                print('rowcount =', self.cursor.rowcount)
        except mysql.connector.errors.ProgrammingError:
            print("数据库错误")

    def commit(self):
        self.conn.commit()
        self.cursor.close()






    #获取自增长的值
    def getID(self):
        sql="""
             SELECT MAX( id ) FROM  `phome_ecms_news_index` 
        """
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql)
        values = self.cursor.fetchall()
        # self.cursor.close()
        # print(values)
        return values[0][0]



    def updategetidpath(self,classiD):
        sql = """
                  SELECT classpath FROM `phome_enewsclass` WHERE `classid`={}
            """.format(classiD)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        values = cursor.fetchall()

        return values[0][0]

        # CLASSID栏目id
    def insert_news_index(self, classid):
        sql = "INSERT INTO `empirecms`.`phome_ecms_news_index` (`id`, `classid`, `checked`, `newstime`, `truetime`, `lastdotime`, `havehtml`) VALUES (NULL, '{}', '1', '{}','{}', '{}', '0')".format(classid, self.nowintdate, self.nowintdate, self.nowintdate)
        # print(sql)

        self.commit_sql(sql)
        self.commit()

    def insert_news_data_1(self, id, classid, author, beform, content):
        sql = "INSERT INTO `empirecms`.`phome_ecms_news_data_1` (`id`, `classid`, `keyid`, `dokey`, `newstempid`, `closepl`, `haveaddfen`, `infotags`, `writer`, `befrom`, `newstext`) VALUES ('{}', '{}', '', '1', '0', '0', '0', '', '{}', '{}', '{}')".format(id, classid, author, beform, content)
        # print(sql)
        self.commit_sql(sql)

    def insert_news(self,classid,title,desc):
        date=str(self.i.year)+"-"+str(self.i.month)+"-"+str(self.i.day)

        titleurl="/cms/{}/{}/{}.html".format(self.updategetidpath(classid),date,self.getID())
        # print(titleurl)
        sql="""INSERT INTO `empirecms`.`phome_ecms_news` (`id`, `classid`, `ttid`, `onclick`, `plnum`, `totaldown`, `newspath`, `filename`, `userid`, `username`, `firsttitle`, `isgood`, `ispic`, `istop`, `isqf`, `ismember`, `isurl`, `truetime`, `lastdotime`, `havehtml`, `groupid`, `userfen`, `titlefont`, `titleurl`,`stb`, `fstb`, `restb`, `keyboard`, `title`, `newstime`, `titlepic`, `eckuid`, `ftitle`, `smalltext`, `diggtop`) VALUES (NULL,  '{}', '0', '1', '0', '0', '{}','{}','1','admin','0',  '0','0','0','0', '0',  '0','{}','{}', '0','0','0',  '',  '{}', '1',  '1','1',  '',  '{}',   '{}', '', '0',  '', '{}', '0')""".format(classid,date,self.getID(),self.nowintdate,self.nowintdate,titleurl,title,self.nowintdate,desc)
        # print(sql)
        self.commit_sql(sql)

    def close(self):
        self.cursor.close()
        self.conn.close()
    def phome_enewsclass(self,clasid):
        sql="update phome_enewsclass set allinfos=allinfos+1,infos=infos+1 where classid='{}' limit 1".format(clasid)
        self.commit_sql(sql)


    def phome_enewspublic_up(self):
        sql="update phome_enewspublic_up set lastnuminfo=lastnuminfo+1,lastnuminfotb='|1,3|',todaynuminfo=todaynuminfo+1 limit 1"
        self.commit_sql()
        #

    #查询重复
    def find_titile(self,classid,content):
        sql=" SELECT * FROM  `phome_ecms_news` WHERE  `classid` =' {} ' And `title`=  '{}' ".format(classid,content)
        # print(sql)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        values = cursor.fetchall()
        # print(values)
        if(values!=[]):
             return True
        if(values==[]):
            return False
        # if(values==[]):
        #     return True
        # else:
        #     return False
        # self.cursor.close()
        # print(values)
        # return values[0][0]
        # if (self.cursor.rowcount == 1):
        #     return  True;
        # else:
        #     return False


    def rolback(self):
        self.conn.rollback()
        self.cursor.close()

    def rm_id(self):
        sql="""
        DELETE FROM phome_ecms_news_index WHERE id NOT IN (
SELECT id
FROM phome_ecms_news_data_1
)
        
        """
        self.commit_sql(sql)


if __name__ == '__main__':
    print("db class ")
    # x=InsertDB()
    # x.insert_news_index(1)
    # x.insert_news(1,"234","1+1")
    # x.insert_news_data_1(x.getID(),1,"张三","新华网","777")
    # x.commit()
    # x.close()