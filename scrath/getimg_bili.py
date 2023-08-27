# getimg_bili.py
# Author: Sonder M. W.
# Created : 7th April 2022
# Version : 0.1.2

"""
Description :

This script will get images from the homepage of a user in B.
"""

from pathlib import Path
import shutil

from icecream import ic
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup


heidashuai = "294675228"
tiangoujianchaguan = "3461572714301841"
jiulangxianren = "505390315"  # (drop)

itsBettermie = "192357439"
tongnainainainai = "23571162"
jenny = "111060699"


bili_id = tiangoujianchaguan


def get_total_page():
    userinfo_url = f"https://space.bilibili.com/{bili_id}/video"
    session = HTMLSession()
    response = requests.get(userinfo_url)
    html = response.content.decode("utf-8", "ignore")
    soup = BeautifulSoup(response.text, "html.parser")
    # response.encoding
    ic(soup.find("span", {"class": "be-pager-total"}))
    # response.html.render()
    # ic(response.html.html)
    # total_page = response.html.find("span.be-pager-total", first=True).text
    # return ic(total_page[2:-3])
    return 3


def get_image_urls():
    total_page = get_total_page()
    ic(total_page)
    base_url = "https://api.bilibili.com/x/space/arc/search?mid={0}&ps=30&tid=0&pn={1}&keyword=&order=pubdate&jsonp=jsonp"
    session = HTMLSession()
    # for i in range(1, get_total_page()+1):
    for i in range(1, 2):
        url = base_url.format(bili_id, i)
        response = session.get(url, stream=True)
        print(response.json())
        for i in response.json()["data"]["list"]["vlist"]:
            print(i)
            yield {"name": i["title"], "url": f'{i["pic"]}'}


def remove_unvalid_chars(s):
    for c in r""""'<>/\|:*?""":
        s = s.replace(c, "")
    return s


def download_images(dir: str):
    folder = Path(dir).expanduser()
    if not folder.exists():
        folder.mkdir()

    for i in get_image_urls():
        response = requests.get(i["url"], stream=True)
        filename = remove_unvalid_chars(i["name"]) + ".jpg"
        with open(folder / filename, "wb") as f:
            shutil.copyfileobj(response.raw, f)
        print(f'{i["name"]}.jpg is finished.')


if __name__ == "__main__":
    save_folder = r"~/Pictures/images"
    download_images(save_folder)
