from selenium import webdriver
from Database import Databases
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium
from urllib.parse import urlparse
from selenium.webdriver import ActionChains
from typing import *
from urllib.parse import urljoin, urlencode, urlparse, urlunparse
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException

class DownloadHTML():
    def __init__(self, driver):
        self.driver = driver

    def downloadHTML(self, driver, hostname, url):
        print(">>")
        # check driver status
        time.sleep(3)
        driver.get(url)
        return (hostname, url, driver.page_source)


    def saveToDatabase(self, db: Databases, hostname, url, body):
        db.insertNaverBlogBody(hostname, url, body)
        return