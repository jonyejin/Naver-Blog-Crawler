# Naver Blog Crawler

**주의! 모든 법적인 책임은 크롤링을 하는 본인에게 있습니다.**
**위 코드는 학습용으로 개발 되었습니다.**

### Introduction

`Naver Blog Crawler`은 대량의 네이버 블로그 포스팅을 수집하는 라이브러리입니다. 간단하게 한국어 블로그 데이터셋을 구성하도록 도와줍니다. Chrome Driver와 Selenium을 통해 간단하게 사용할 수 있습니다.


### Setup
* Chrome Driver 설치하기
    - [`Chrome Driver`](https://chromedriver.chromium.org/downloads)중 사용자 OS와 맞는 드라이버를 다운받아 최상단 폴더에 넣습니다.
    - `main.py`의 driver PATH를 driver가 저장된 절대경로로 바꿔줍니다. 

* (Optional) Database 연결하기
    - 위 프로젝트는 `Postgresql`에 데이터를 저장하는 형태로 개발되었습니다. `Secrets.py`파일을 만들어서 `SECRET_HOST`, `SECRET_DBNAME`, `SECRET_USER`, `SECRET_PASSWORD`, `SECRET_PORT` 변수를 채워줍니다.

### Crawl Blog Path
[네이버 블로그 주제별보기](https://section.blog.naver.com/ThemePost.naver?directoryNo=0&activeDirectorySeq=0&currentPage=1) 에서 5가지 탭에서 추천된 블로그 HOST명을 크롤링해서 데이터베이스에 저장합니다. 
총 3개의 파라미터를 합쳐서 Path가 완성됩니다.
directoryNo={}&activeDirectorySeq={}&currentPage={}
한 페이지에는 10개의 포스팅이 존재합니다. currentPage가 존재하는 페이지 개수보다 크면 가장 마지막 페이지 내용을 리턴합니다.

- 관심주제: directoryNo=0&activeDirectorySeq=0 (100페이지)
- 엔터테인먼트&예술:activeDirectorySeq=1 
    - 문학,책: directoryNo=5
    - 영화: directoryNo=6
    - 미술,책: directoryNo=8
    - 공연,전시: directoryNo=7
    - 음악: directoryNo=11
    - 드라마: directoryNo=9
    - 스타, 연예인:directoryNo=12
    - 만화, 애니: directoryNo=13
    - 방송: 10
- 생활,노하우,쇼핑: activeDirectorySeq=2
    - 일상,생각: 14
    육아,결혼: 15
    반려동물: 16
    좋은글,이미지: 17
    패션,미용: 18
    인테리어,DIY: 19
    요리,레시피: 20
    상품리뷰: 21
    원예,재배: 36
- 취미,여가,여행: activeDirectorySeq=3
    - 게임: 22
    - 스포츠: 23
    - 사진: 24
    - 자동차: 25
    - 취미: 26
    - 국내여행: 27
    - 세계여행: 28
    - 맛집: 29
- 지식,동향: activeDirectorySeq=4
    - IT,컴퓨터: 30
    - 사회,정치:31
    - 건강,의학:32
    - 비즈니스,경제:33
    - 어학,외국어:35
    - 교육,학문: 34

(ex) IT,컴퓨터 1페이지: https://section.blog.naver.com/ThemePost.naver?directoryNo=4&activeDirectorySeq=30&currentPage=1

### Dependencies
* beautifulsoup4
* urllib3
* selenium
* psycopg2