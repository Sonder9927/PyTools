# getimg_bili.py
# Created : 7th April 2022
# Last modified : 17th April 2022
# Version : 1.0.1

'''
Description :

This script will get images from the homepage of a user in B.
'''
# just checking
_author_ = "Winona"

from requests_html import HTMLSession

userinfo_url = 'https://space.bilibili.com/192357439/video'
save_folder = r'~/Pictures/images'

def get_total_page():
    session = HTMLSession()
    response = session.get(userinfo_url)
    response.html.render()
    total_page = response.html.find('span.be-pager-total', first=True).text
    return int(total_page[2:-3])

def get_image_urls():
    base_url = 'https://api.bilibili.com/x/space/arc/search?mid=192357439&ps=30&tid=0&pn={0}&keyword=&order=pubdate&jsonp=jsonp'
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
    import pathlib
    import requests
    import shutil

    folder = pathlib.Path(save_folder).expanduser()
    if not folder.exists():
        folder.mkdir()

    for i in get_image_urls():
        response = requests.get(i["url"], stream=True)
        filename = remove_unvalid_chars(i['name']) + '.jpg'
        with open(folder/filename, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        print(f'{i["name"]}.jpg is finished.')

download_images()
