from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
import unicodedata
import time


driver = webdriver.Chrome(executable_path='chromedriver_path')
# 웹 접속
def web_load(url):
    driver.get(url)
    time.sleep(3)

# 로그인 메소드
def insta_login(id, pwd):
    driver.find_element_by_name('username').send_keys(id)
    driver.find_element_by_name('password').send_keys(pwd)
    driver.find_element_by_class_name('Igw0E.IwRSH.eGOV_._4EzTm.bkEs3.CovQj.jKUp7.DhRcB').click()
    
    # 대기타임
    time.sleep(3)

# 인스타 탐색 메소드
def insta_searching(word):
    url = 'https://www.instagram.com/explore/tags/' + word
    driver.get(url)
    time.sleep(3)
    return url
# 인스타그램 나중에하기 클릭 메소드
def insta_click_later_button():
    driver.find_element_by_class_name('sqdOP.yWX7d.y3zKF').click()
    time.sleep(1)
    # 아이디, 패스워드 저장여부 패스
    try:
        driver.find_element_by_class_name('aOOlW.HoLwm').click()
    except:
        pass

# 인스타그램 왼쪽 상단 이미지 클릭
def insta_click_first():
    driver.find_element_by_css_selector("div._9AhH0").click()
    time.sleep(3)

# 인스타그램 내용 가져오기
def insta_get_content(driver):
    # 1. 현재 페이지의 HTML정보 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    
    # 2. 본문 내용 가져오기
    try:
        content = soup.select('div.C4VMK > span')[0].text
        
        content = unicodedata.normalize('NFC', content)
    except:
        content = ''
    
    # 3. 본문 내용에서 해쉬태그 가져오기(정규식 사용)
    try:
        tags = re.findall(r'#[^s#,\\]+', content)
    except:
        tags = ''
    # 4. 작성일자 정보 가져오기
    date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10]

    # 5. 좋아요 수 가져오기
    try:
        like = soup.select('div.Nm9Fw > button')[0].text[4:-1]
    except:
        like = 0

    # 6. 위치정보 가져오기
    try:
        place = soup.select('a.O4GlU')[0].text
        place = unicodedata.normalize('NFC', place)
    except:
        place = ''
    
    # 7. 수집한 정보 저장하기
    data = [content, date, like, place, tags]
    return data

def move_next(driver):
    driver.find_element_by_css_selector('a.coreSpriteRightPaginationArrow').click()
    time.sleep(3)


web_load('https://www.instagram.com/accounts/login/')

insta_login('', '')

insta_click_later_button()

insta_searching('제주도맛집')

insta_click_first()

insta_results = []

target = 500

for i in range(target):
    #게시글 수집에 오류 발생 시 2초 대기 후
    #다음 게시글로 넘어가도록 try, except 구문을 활용

    try:
        data = insta_get_content(driver)
        insta_results.append(data)
        move_next(driver)
    except:
        time.sleep(2)
        move_next(driver)

driver.close()


print(insta_results[:2])

results_df = pd.DataFrame(insta_results)

results_df.columns = ['content', 'date', 'like', 'place', 'tags']

results_df.to_excel('insta_jeju_Matzip.xlsx', index=False)
