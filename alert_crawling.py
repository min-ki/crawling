from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graduate_or_continue.settings")

import django
django.setup()

from parsed_data.models import Subject

def parsed_subject():
    driver = webdriver.Chrome("/Users/k352ex/Downloads/Chromedriver")
    # driver.implicitly_wait(3)
    driver.get("http://intra.wku.ac.kr/SWupis/V005/login.jsp")


    # 로그인을 위한 id, pw 정보
    driver.find_element_by_name('userid').send_keys('')
    driver.find_element_by_name('passwd').send_keys('')
    driver.find_element_by_xpath("//*[@id = 'f_login']/fieldset/dl/dd[3]/input").click()

    try:
        WebDriverWait(driver, 1).until(EC.alert_is_present(), "test")
        alert = driver.switch_to_alert()
        alert.accept()
        print("alert accepted")
    except TimeoutException:
        print("no alert")

    driver.get("http://intra.wku.ac.kr/SWupis/V005/Service/Stud/Score/scoreAll.jsp?sm=3")

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')


    select_year = soup.select('body > table > tbody > tr > td:nth-of-type(6) > a')

    year_list = []

    for item in select_year:
        year_list.append(item)

    subject = []

    for x in year_list:
        driver.get("http://intra.wku.ac.kr" + x['href'])
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        subject_list = soup.select('body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(3)')
        # body > table:nth-child(4) > tbody > tr:nth-child(2) > td:nth-child(3)
        for item in subject_list:
            subject.append(item.text)

    return subject

if __name__=='__main__':
    sub = parsed_subject()

    for item in sub:
        Subject(title=item).save()
