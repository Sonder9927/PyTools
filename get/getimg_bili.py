# getimg_bili.py
# Author: Sonder M. W.
# Created : 7th April 2022
# Version : 0.1.2

'''
Description :

This script will get images from the homepage of a user in B.
'''
# just checking

from requests_html import HTMLSession
from pathlib import Path
import requests
import shutil


heidashuai = "192357439"


bili_id = heidashuai

userinfo_url = f'https://space.bilibili.com/{bili_id}/video'
save_folder = r'~/Pictures/images'

def get_total_page():
    session = HTMLSession()
    response = session.get(userinfo_url)
    response.html.render()
    total_page = response.html.find('span.be-pager-total', first=True).text
    return int(total_page[2:-3])

def get_image_urls():
    base_url = f'https://api.bilibili.com/x/space/arc/search?mid={bili_id}&ps=30&tid=0&pn={0}&keyword=&order=pubdate&jsonp=jsonp'
    session = HTMLSession()
    for i in range(1, get_total_page()+1):
        url = base_url.format(i)
        response = session.get(url)
        for i in response.json()['data']['list']['vlist']:
            print(i)
            yield {'name':i['title'], 'url': f'{i["pic"]}'}

def remove_unvalid_chars(s):
    for c in r'''"'<>/\|:*?''':      
        s = s.replace(c, '')
    return s

def download_images():
    folder = Path(save_folder).expanduser()
    if not folder.exists():
        folder.mkdir()

    for i in get_image_urls():
        response = requests.get(i["url"], stream=True)
        filename = remove_unvalid_chars(i['name']) + '.jpg'
        with open(folder/filename, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        print(f'{i["name"]}.jpg is finished.')


if __name__ == "__main__":
    download_images()

