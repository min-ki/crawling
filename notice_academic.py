# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
from string import digits

'''
    공지사항 - 학사공지
'''

driver = webdriver.Chrome("/Users/k352ex/Downloads/Chromedriver")
driver.implicitly_wait(3)

driver.get("http://www.wku.ac.kr/category/notice/academic-notice") # 학사공지
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

academic_notice_url = "http://www.wku.ac.kr/category/notice/academic-notice/page/"
last_page = soup.select("#content > div.pagination > a")
last_page = last_page[-2].text

for i in range(1, int(last_page) + 1):
    driver.get(academic_notice_url + str(i))
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    notice_academic_title = soup.select('#content > div.postList > ul > li > a > strong')
    notice_academic_meta = soup.select('#content > div.postList > ul > li > span.meta')
    notice_academic_date = soup.select('#content > div.postList > ul > li > span.meta > span')
    notice_academic_post_url = soup.select('#content > div.postList > ul > li > a')

    for t, d, m, u in zip(notice_academic_title, notice_academic_date, notice_academic_meta, notice_academic_post_url):

        remove_digits = str.maketrans('', '', digits)
        m = m.text.translate(remove_digits).replace('/', '')

        print("제목: " + t.text.strip())
        print("날짜: " + d.text.strip())
        print("작성: " + m)

        driver.get(u['href'])
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        post_content = soup.select(
            '#content > table > tbody > tr > td > p > a > img')

        if not post_content:
            post_content = soup.select('#content > table > tbody > tr > td')

            content = ""

            for item in post_content:
                if item:
                    content += item.text

            print(content.strip())
            print("")
            print('-' * 30)
            print("")

        else:

            print(post_content)
