#-*- codind: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
from string import digits
"""
    공지사항 - 장학공지
    모든 공지사항 제목, 날짜, 작성, 본문 크롤링
"""


driver = webdriver.Chrome("/Users/k352ex/Downloads/Chromedriver")
driver.implicitly_wait(3)

driver.get("http://www.wku.ac.kr/category/notice/scholar-notice/")
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

scholar_notice_url = "http://www.wku.ac.kr/category/notice/scholar-notice/page/"
last_page = soup.select("#content > div.pagination > a")
last_page = last_page[-2].text

for i in range(1, int(last_page) + 1):
    driver.get(scholar_notice_url + str(i))

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    notice_scholar_title = soup.select('#content > div.postList > ul > li > a > strong')
    notice_scholar_meta = soup.select('#content > div.postList > ul > li > span.meta')
    notice_scholar_date = soup.select('#content > div.postList > ul > li > span.meta > span')
    notice_scholar_post_url = soup.select('#content > div.postList > ul > li > a')
    

    for t, d, m, u in zip(notice_scholar_title, notice_scholar_date, notice_scholar_meta, notice_scholar_post_url):

        remove_digits = str.maketrans('','', digits)
        m = m.text.translate(remove_digits).replace('/', '')
        
        print("제목: " + t.text.strip())
        print("날짜: " + d.text.strip())
        print("작성: " + m)

       

        driver.get(u['href'])
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        post_content = soup.select('#content > table > tbody > tr > td')

        content = ""
        
        for item in post_content:
            content += item.text
        
        print(content.strip())
        print("")
        print('-' * 30)
        print("")

