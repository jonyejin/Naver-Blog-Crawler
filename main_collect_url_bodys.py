from selenium import webdriver
from selenium.webdriver.common.by import By

from Database import Databases
from DownloadHTML import DownloadHTML
from AdressCollecting import *
import urllib.request as req
import re
import time
import os
import ssl

# 인증서 문제 해결
ssl._create_default_https_context = ssl._create_unverified_context

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--no-sandbox')
options.add_argument("disable-gpu")
options.add_argument('window-size=1920x1080')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

driver = webdriver.Chrome(r'/home/dilab/Documents/GitHub/Naver-Blog-Crawler/chromedriver', options = options)
driver.set_window_position(0, 0)
# driver.maximize_window()
driver.set_window_size("1879", "2427")


# Database
db = Databases()
downloader = DownloadHTML(driver)

# Naver Blog 주소 수집용
# print(naver_blog_recommendation(driver=driver, database=db, callback_function=db.insertNaverBlogLink))


# Naver Blog 본문 수집용
# url이 저장되어 있을 때 중복되지 않게 불러와서 naver blog url리스트를 만들고 
# 각각에 대해서 download하고 다시 db에 저장해준다.

def collect_posting_urls():
    value = 10003
    limit = 1000
    try:
        while True:
            urls = db.selectNaverBlogLink(offset=value, limit=1) # List 
            print(urls)

            # 원래는 개수를 비교해야 하지만...
            if urls == []:
                break

            for url_packed in urls:
                u = url_packed[0] # 
                print(u)
                id = u.lstrip('https://blog.naver.com/').split('/')[0]
                all_post_url = f"https://blog.naver.com/PostList.naver?blogId={id}&categoryNo=0&from=postList"
                print(all_post_url)
                driver.get(all_post_url)
                
                #목록 열기 해서 주소만 수집한다.
                naver_blog_posts(driver, database=db, callback_function=None)
            value += limit
    except Exception as e:
        print(e)
        print('여기에요 여기')
        # print(e)

def collect_url_bodys():
    value = 0
    limit = 100
    try:
        while True:
            urls = db.selectNaverBlogPageLink(offset=value, limit=limit) # List 

            # 원래는 개수를 비교해야 하지만...
            if urls == []:
                break

            for url_packed in urls:
                u = url_packed[0] # 
                print(u)
                try:
                    (_hostname, _url, _page_source) = downloader.downloadHTML(driver=driver, hostname=naverBlogAddressToHostname(u), url=u)
                except UnexpectedAlertPresentException:
                    continue
                db.insertNaverBlogBody(hostname=naverBlogAddressToHostname(u), url=u, body=_page_source)
            value += limit
        

    except Exception as e:
        print(e)
        print('여기에요 여기')
        # print(e)


collect_url_bodys()