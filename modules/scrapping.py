import re
import urllib.request
import urllib.parse
from urllib.error import URLError

import requests
from bs4 import BeautifulSoup

import time

from selenium import webdriver

import math

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


def kakao(search):
    url = urllib.parse.quote("https://m.map.kakao.com/actions/searchView?q=" + search + "&wxEnc=LVSOTP&wyEnc=QNLTTMN&lvl=4", safe=':/?=&')
    print(url)

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    store_list = []
    store_dict = {}
    # find = soup.find_all('ul', 'search_list _items')
    find = soup.find_all('li', 'search_item base')
    print(find)
    for store in find:
        print(store.attrs)
        img_text = ""
        addr_text = ""
        img = store.find('img')
        if img:
            # print(img.attrs)
            img_text = img.attrs['src']
        addr = store.find('span', 'txt_g')
        if addr:
            # print(addr.text)
            addr_text = addr.text
        # store_dict['id'] = store.attrs['data-id']
        # store_dict['title'] = store.attrs['data-title']
        # store_dict['phone'] = store.attrs['data-phone']
        # store_dict['img'] = img_text
        # store_dict['addr'] = addr_text
        # print(store_dict)
        # 가게 ID, 가게 이름, 가게 전화번호(제거), 대표 이미지, 주소
        # store_list.append([store.attrs['data-id'], store.attrs['data-title'], store.attrs['data-phone'], img_text, addr_text])
        store_list.append({'id': store.attrs['data-id'], 'title': store.attrs['data-title'], 'img': img_text, 'addr': addr_text})
        print(store_list)

    print(store_list)
    return store_list


def review(store_id):
    # Chrome 창 숨기기
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome(options=options)

    # 카카오맵 URL (PC버전)
    # url = 'https://place.map.kakao.com/m/2141491711#comment'
    url = 'https://place.map.kakao.com/' + str(store_id) + '#comment'

    driver.get(url)

    reviews = []

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(0.4)

        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        tmp = driver.page_source
        tmp2 = BeautifulSoup(tmp, "html.parser")

        total_reviews = int(
            tmp2.select('#mArticle > div.cont_evaluation > strong.total_evaluation > span')[0].get_text())
        pages = math.ceil(total_reviews / 5)
        print(pages)
        time.sleep(0.4)

    for i in range(1, pages + 1):

        i = i + 1

        if i > pages:
            break

        # 후기 더보기 버튼 클릭
        # next_page = driver.find_element(By.XPATH, "//a[@data-page='" + str(i) + "']")
        next_page = driver.find_element(By.CSS_SELECTOR, '#mArticle > div.cont_evaluation > div.evaluation_review > a')
        next_page.send_keys(Keys.ENTER)
        time.sleep(0.2)

    time.sleep(0.5)
    t1 = driver.page_source
    t2 = BeautifulSoup(t1, "html.parser")

    store_name = t2.select_one('.tit_location').text

    t3 = t2.find(name="div", attrs={"class": "evaluation_review"})

    review_all = t3.find_all('p', {'class': 'txt_comment'})

    reviews.extend(review_all)

    driver.close()

    str_reviews = list(map(str, reviews))
    print(str_reviews)

    p = re.compile('<span>(.*)</span>')
    filtered_reviews = []
    for r in str_reviews:
        review = p.findall(r)[0]
        if review != '':
            # review = review.replace('<br/>', '\n')
            review = review.replace('\t', ' ')
            filtered_reviews.append(review)

    f = open('modules/input.tsv', 'w', encoding='utf-8')
    f.write('\treview\n')
    for i in range(len(filtered_reviews)):
        data = str(i) + '\t' + filtered_reviews[i] + '\n'
        f.write(data)
    f.close()

    return store_name
