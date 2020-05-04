import requests
import time
from bs4 import BeautifulSoup
import os
import re
import urllib.request
import json

#目的：找到價錢大於2000美金的外套，並將圖片下載下來
#func 1 => 找到get_web_page(url) return resp.text:
#func 2 => 進入每一頁(共39頁)去parse所有檔案，return data(品牌名、品牌項目、價錢、圖片連結)
#func 3 => 進入每一個href，並下載圖片
# main Func => 判斷下載下來的所有檔案裡的價錢要大於2000每的才會使用func 3去下載圖片

url = "https://www.ssense.com/en-tw/men/jackets-coats"

def get_web_page(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text

def enter_every_page(dom):
    items = []
    soup = BeautifulSoup(dom,"html5lib")
    all_items = soup.find_all("figure","browsing-product-item")
    for item in all_items:
        brand_name = item.find("p","bold").text.strip()
        item_name = item.find("p","product-name-plp").text.strip()
        price = item.find("span","price").text.replace("$","")
        item_pic_link = item.find_all("meta")[1]["content"] #item.find("picture").find("source", {'media': "(min-width: 1025px)"})["srcset"]
        items.append({
            "brand_name":brand_name,
            "item_name":item_name,
            "price":price,
            "item_pic_link":item_pic_link
        })
    for i in range(2,39+1):
        new_dom = get_web_page(url + "?page="+str(i))
        if new_dom:
            soup = BeautifulSoup(new_dom, "html5lib")
            all_items = soup.find_all("figure", "browsing-product-item")
            for item in all_items:
                brand_name = item.find("p", "bold").text.strip()
                item_name = item.find("p", "product-name-plp").text.strip()
                price = item.find("span", "price").text.replace("$", "")
                item_pic_link = item.find_all("meta")[1][
                    "content"]  # item.find("picture").find("source", {'media': "(min-width: 1025px)"})["srcset"]
                items.append({
                    "brand_name": brand_name,
                    "item_name": item_name,
                    "price": price,
                    "item_pic_link": item_pic_link
                })
    return items

def save(img_url, title):  #下載連結
    if img_url:
        try:
            dname = title.strip()  # 用 strip() 去除字串前後的空白
            if not os.path.exists(dname):
                os.makedirs(dname)
            fname = img_url.split('/')[-1]  # 將網址的最後的名稱設為檔案名稱
            urllib.request.urlretrieve(img_url, os.path.join(dname, fname))
                    #使用urllib.request.urlretrieve(檔案夾名, 檔案名)這個func把圖片下載下來到資料夾裡
        except Exception as e:
            print(e)

if __name__ == '__main__':
    if get_web_page(url):
        all_items = enter_every_page(get_web_page(url))
        print(all_items)

        for i in range(0,len(all_items)-1):
            if int(all_items[i]["price"]) >= 2000:
                single_title = all_items[i]["brand_name"]
                single_href = all_items[i]["item_pic_link"]

                save(single_href, single_title)
