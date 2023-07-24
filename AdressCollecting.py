import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium
from urllib.parse import urlparse
from selenium.webdriver import ActionChains
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
import selenium
from urllib.parse import urlparse
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 네이버 블로그 메인 추천에서 찾기
def naver_blog_recommendation(driver, database, callback_function):
    directoryNoKV = {#0:[0],
                    1: [6,8,7,11,9,12,13], 
                    2: [14, 15, 16, 17, 18, 19, 20, 21, 36], #5
                    3: [22, 23, 24, 25, 26, 27, 28, 29], 
                    4: [30, 31, 32, 33, 35, 34]}
    
    for activeDirectorySeq in range(1, 5):
        for directoryNo in directoryNoKV[activeDirectorySeq]:
            url = f"https://section.blog.naver.com/ThemePost.naver?activeDirectorySeq={activeDirectorySeq}&directoryNo={directoryNo}&currentPage=1" # 
            while True:
                max_other_button = 0
                print(url)
                # 먼저 페이지 이동하기
                driver.get(url)
                time.sleep(3)

                # 일단 현재 페이지 파싱
                blogs = driver.find_elements(By.XPATH, "//a[@class='desc_inner']")
                for n in blogs:
                    print(n.get_attribute('href'))
                    h = "/".join(n.get_attribute('href').split("/")[:-1])
                    database.insertNaverBlogLink(h, n.get_attribute('href'))

                # pagination 대응하기
                # 현재 <strong>태그 다음 버튼을 클릭한다. 없다면 break.
                    # 1, 2, 3, 현재 페이지, 4, ...10, 다음페이지
                try: 
                    현재_페이지_아닌_버튼들 = driver.find_elements(By.XPATH, ".//a[@ng-if='currentPage!=page']") # 9개
                    현재_페이지_버튼 = driver.find_element(By.XPATH, ".//a[@ng-if='currentPage==page']") # 1개
                    현재_페이지 = int(현재_페이지_버튼.text)
                    
                    print(max_other_button)
                    
                    for b in 현재_페이지_아닌_버튼들:
                        max_other_button = int(b.text) if int(b.text) > max_other_button else max_other_button
                        if int(b.text) == (현재_페이지 + 1):
                            url = f"https://section.blog.naver.com/ThemePost.naver?directoryNo={directoryNo}&activeDirectorySeq={activeDirectorySeq}&currentPage={b.text}" # 
                            break
                    
                    print(max_other_button)

                    # 다음으로 넘어갈 페이지 없는 상황: 다음페이지버튼 존재하는지 확인
                    if max_other_button < 현재_페이지:
                        try:
                            next_btn = driver.find_element(By.CLASS_NAME, "button_next")
                            url = f"https://section.blog.naver.com/ThemePost.naver?directoryNo={directoryNo}&activeDirectorySeq={activeDirectorySeq}&currentPage={현재_페이지+1}"
                            
                        except NoSuchElementException:
                            print("next button 없음")
                            # 다음 카테고리로 넘어간다.
                            break

                except Exception as e:
                    print(e)
                    print(f"???/{e}")


# 목록 열기 해서 주소를 수집한다.
def naver_blog_posts(driver, database, callback_function):
    try:
        # pagination 대응하기
        # 현재 <strong>태그 다음 버튼을 클릭한다. 없다면 break.
        while True:
            time.sleep(5)

            # 목록 열기
            try:
                # 일단 목록열기 클릭
                time.sleep(1)
                목록열기 = driver.find_element(By.XPATH, "//span[@id='toplistSpanBlind']")
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(목록열기))
                if 목록열기.text == "목록열기":
                    목록열기.click()
                time.sleep(2)
            except Exception as e:
                print("목록열기 없음") # 작성된 글이 하나도 없을 때 발생 (ex: https://blog.naver.com/PostList.naver?blogId=1224&categoryNo=0&from=postList)
                print(e)
                break 
            
            # 10개의 버튼들마다 5개의 링크를 수집한다.
            try:
                index_buttons_without_current = driver.find_elements(By.XPATH, "//a[contains(@class, 'page pcol2')]")
                button_num = len(index_buttons_without_current)
                for i in range(1, button_num+1):
                    print(i)
                    # 나를 제외한 페이지 버튼 찾기
                    index_buttons_without_current = driver.find_elements(By.XPATH, "//a[contains(@class, 'page pcol2')]")

                    # 목록에 보여지는 url들 저장하기
                    urls = driver.find_elements(By.XPATH, "//a[contains(@class, 'pcol2 _setTop _setTopListUrl')]")
                    for u in urls:
                        page_url = u.get_attribute('href')
                        database.insertNaverBlogUrl('', page_url, '')

                    if i == button_num:
                        break
                    else:
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(index_buttons_without_current[i]))
                        index_buttons_without_current[i].click()
                        time.sleep(2)

            except NoSuchElementException:
                print(f"다음 페이지 버튼이 존재하지 않는다")
                break
            
            except IndexError:
                print("index out of range")
                break
            except Exception as e:
                print("??")
                print(e)
            
            # 다음 버튼 누르기
            try:
                # 이미 10페이지이면 다음 버튼 클릭
                # 다음 버튼 찾기
                print("다음 버튼 찾기")
                if driver.find_element(By.XPATH, "//span[@id='toplistSpanBlind']").text == "목록열기":
                    # 일단 목록열기 클릭
                    print("목록을 다시 열었다")
                    목록열기 = driver.find_element(By.XPATH, "//span[@id='toplistSpanBlind']")
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(목록열기))

                #혹시라도 목록이 닫혀있다면 열어준다


                next_button = driver.find_element(By.XPATH, "//a[contains(@class, 'next pcol2')]")
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(next_button))
                next_button.click()
                time.sleep(2)
                continue

            except IndexError:
                print("페이지 끝까지 다 봄")
                break
            except ElementNotInteractableException:
                print("next 버튼이 클릭이 안됨")
                break
            except NoSuchElementException:
                print(f"Next Button이 없는 경우.")
                break

    except Exception as e:
        print(e)


# 네이버 블로그 주소를 hostname만 남긴다
def naverBlogAddressToHostname(url: str):
    id = urlparse(url).query.split('&')[0].split('=')[1]
    return f"https://blog.naver.com/{id}"
