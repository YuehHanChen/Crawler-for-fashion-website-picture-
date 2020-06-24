import requests
import time
from bs4 import BeautifulSoup
import os
import re
import urllib.request
import json

#Goal：Find all the jackets that the prices are above $2000 usd, and download the pictures.
#func 1 => find "get_web_page(url)" return resp.text:
#func 2 => Go to each page(39 pages in total), and parse all files, then return data(Brand name, item name, price, url of the picture)
#func 3 => Enter each url and then download pictures.
# main Func => Determine whether the price is above $2000, if so, then func 3 to download the picture

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

def save(img_url, title):  #Download the link
    if img_url:
        try:
            dname = title.strip()  # 用 strip() delete the blank in front of or in the back of the string
            if not os.path.exists(dname):
                os.makedirs(dname)
            fname = img_url.split('/')[-1]  # set last string of url as file name
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
