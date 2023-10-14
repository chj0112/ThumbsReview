import re
import urllib.request
import urllib.parse
from urllib.error import URLError

import requests
from bs4 import BeautifulSoup


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
        # 가게 ID, 가게 이름, 가게 전화번호, 대표 이미지, 주소
        # store_list.append([store.attrs['data-id'], store.attrs['data-title'], store.attrs['data-phone'], img_text, addr_text])
        store_list.append({'id': store.attrs['data-id'], 'title': store.attrs['data-title'], 'phone': store.attrs['data-phone'], 'img': img_text, 'addr': addr_text})
        print(store_list)

    print(store_list)
    return store_list
