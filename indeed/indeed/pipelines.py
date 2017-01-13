# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql.cursors
import datetime
from indeed.items import IndeedItem, JobItem

class IndeedPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost',
                                    user='user',
                                    password='pwd',
                                    db='database',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor
                                    )

    def process_item(self, item, spider):
        #print(item['JobTitle'], item['Location'])
        curTime = datetime.datetime.now()
        if isinstance(item, IndeedItem()):
            ''' Pass job details into JOBs Table.
            '''
            try:
                with self.conn.cursor() as cursor:
                    ''' JobID should be prime key. 
                    Pending issue: 
                    if JobID already exist, it should update the current date.
                    PostDate should be cleaned before insert into SQL.
                    Each item may not be str convertable. Needs more cleaning.
                    '''
                    # insert the record
                    sql = "INSERT IGNORE INTO JOBs (ID, JobTitle, JobUrl, Company, Location, Salary, PostDate, CreatAt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (
                        item['JobID'],
                        item['JobTitle'],
                        item['JobUrl'],
                        item['Company'],   
                        item['Location'],
                        item['Salary'],
                        item['PostDate'],
                        curTime
                        )
                    )
                self.conn.commit()
            except:
                raise KeyError
            finally:
                self.conn.close()
        elif isinstance(item, JobItem):
            ''' Pass Job descriptins into JobDescripotion Table.
            '''
            try:
                with self.conn.cursor() as cursor:
                    sql = "INSERT IGNORE INTO JobDesciption (ID, Description) VALUES (%s, %s)"
                    cursor.execute(sql, (item['JobID'], item('Description')))
                    self.conn.commit()
            finally:
                self.conn.close()


