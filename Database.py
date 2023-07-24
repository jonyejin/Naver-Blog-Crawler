import psycopg2
from typing import List
from Secrets import *

class Databases():
    def __init__(self):
        try:
            self.db = psycopg2.connect(host=SECRET_HOST, dbname=SECRET_DBNAME, user=SECRET_USER,password=SECRET_PASSWORD,port=SECRET_PORT, connect_timeout=3)
            self.cursor = self.db.cursor()
        except psycopg2.DatabaseError as db_err:
            print("Not connected")
            print(db_err)

    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self,query,args={}):
        #print("execute :" + query)
        self.cursor.execute(query,args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.cursor.commit()

    def insertDB(self,schema,table,column,data):
        sql = " INSERT INTO {schema}.{table}(news_key, title, content, reporter_id, pub) VALUES (%s, %s, %s, %s, %s) ;".format(schema=schema,table=table)
        try:
            self.cursor.execute(sql, data)
            #self.db.commit()
        except Exception as e :
            print("insert DB  ",e)
            self.db.rollback()
        else:
            print(data[0])
            self.db.commit()

    # 블로그명
    def insertNaverBlogLink(self, hostname, url):
        schema = "public"
        table = "naver_blogs"
        sql = " INSERT INTO {schema}.{table}(hostname, url) VALUES {sql_str_val} ;".format(schema=schema,table=table, sql_str_val=f"('{hostname}', '{url}')")
        try:
            print(sql)
            self.cursor.execute(sql)
            #self.db.commit()
        except Exception as e :
            print("insert DB  ",e)
            print(sql)
            self.db.rollback()
        else:
            print(sql)
            self.db.commit()

    # 블로그 명 select
    # offset: 시작 위치, limit: 개수
    def selectNaverBlogLink(self, offset:int, limit:int) -> List[tuple]:
        sql = f" SELECT HOSTNAME FROM naver_blogs ORDER BY HOSTNAME, URL DESC LIMIT {limit} OFFSET {offset};"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            if len(result) == 0:
                return
            else: 
                print(result)
                return result
            #self.db.commit()
        except Exception as e :
            print("insert DB  ",e)
            print(sql)
            self.db.rollback()
        else:
            print(sql)
            self.db.commit()

    # 블로그 내 페이지 url select
    # offset: 시작 위치, limit: 개수
    def selectNaverBlogPageLink(self, offset:int, limit:int) -> List[tuple]:
        sql = f" SELECT page_url FROM naver_blog_pages WHERE body is NULL or body='' ORDER BY page_url ASC LIMIT {limit} OFFSET {offset};"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            if len(result) == 0:
                return
            else: 
                print(result)
                return result
            #self.db.commit()
        except Exception as e :
            print("insert DB  ",e)
            print(sql)
            self.db.rollback()
        else:
            print(sql)
            self.db.commit()

    # 블로그 내 page url insert
    def insertNaverBlogUrl(self, hostname, page_url, body):
            schema = "public"
            table = "naver_blog_pages"
           
            sql = " INSERT INTO {table}(hostname, page_url, body) VALUES {sql_str_val} ;".format(table=table, sql_str_val=f"('{hostname}', '{page_url}', '')")
            try:
                # print(sql)
                self.cursor.execute(sql, body)
                #self.db.commit()
            except Exception as e :
                print("DB에서 exception발생")
                print("insert DB  ",e)

                self.db.rollback()
            else:
                # print(sql)
                self.db.commit()

    # 블로그 내 page body update
    def insertNaverBlogBody(self, hostname, url, body):
        schema = "public"
        table = "naver_blog_pages"
        # 특수문자 제거
        body = body.replace("%", '')
        sql = " UPDATE {table} SET body = {body} WHERE page_url = '{url}';".format(table=table, body = f'$YEJIN${body}$YEJIN$', url=url)
        try:
            # print(sql)
            self.cursor.execute(sql)
            #self.db.commit()
        except Exception as e :
            print("DB에서 exception발생")
            print("insert DB  ",e)
            self.db.rollback()
        else:
            # print(sql)
            self.db.commit()