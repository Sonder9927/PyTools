# get image
# Author: Sonder M. W.
# Created : 17th August 2023
# Version : 0.1.2

"""
Description :

This script will get images by url.
"""

from requests_html import HTMLSession
from pathlib import Path
import requests
import shutil


heidashuai = "294675228"
tiangoujianchaguan = "3461572714301841"
jiulangxianren = "505390315"  # (drop)

itsBettermie = "192357439"
tongnainainainai = "23571162"
jenny = "111060699"


bili_id = tiangoujianchaguan


def jenny_0():
    infos = [
        {
            "pic": "http://i1.hdslb.com/bfs/archive/963ef59eaed9b80ff17ab02bdc2858021eb14e81.jpg",
            "title": "Vlog～俺滴五一快乐假期",
        },
        {
            "pic": "http://i0.hdslb.com/bfs/archive/e7162b3207aad0d70200ba7f0c74981229e19ba4.jpg",
            "title": "高中网课日常～开学倒计时1天",
        },
        {
            "pic": "http://i1.hdslb.com/bfs/archive/e77212b4011dbf0248bc79bf8f76f138c17c13bf.jpg",
            "title": "假期vlog｜超级超级喜欢大理哇！",
        },
        {
            "pic": "http://i2.hdslb.com/bfs/archive/ba3f8098a60520ed62e2f7e78eaed4eda91a8312.jpg",
            "title": "【05高二VLOG】高中最后一次运动会啦～",
        },
    ]
    for ii in infos:
        yield {"name": ii["title"], "url": f'{ii["pic"]}'}


def get_total_page():
    userinfo_url = f"https://space.bilibili.com/{bili_id}/video"
    session = HTMLSession()
    response = session.get(userinfo_url)
    response.html.render()
    # print(response.html.html)
    total_page = response.html.find("span.be-pager-total", first=True).text
    print(total_page)
    return int(total_page[2:-3])


def get_image_urls():
    base_url = "https://api.bilibili.com/x/space/arc/search?mid={0}&ps=30&tid=0&pn={1}&keyword=&order=pubdate&jsonp=jsonp"
    session = HTMLSession()
    # for i in range(1, get_total_page()+1):
    for i in range(1):
        url = base_url.format(bili_id, i)
        response = session.get(url)
        jsinfo = response.json()
        print(jsinfo)
        # raise
        for ii in jsinfo["data"]["list"]["vlist"]:
            yield {"name": ii["title"], "url": f'{ii["pic"]}'}


def remove_unvalid_chars(s):
    for c in r""""'<>/\|:*?""":
        s = s.replace(c, "")
    return s


def aola_img_test_url(folder: Path):
    base_url = (
        "http://aola.100bt.com/h5/pet/petskin/background/bg/"
        + "img_petskinbackground_{}.png"
    )
    url = base_url.format("545~202308101691682529")
    aola = {"url": url, "name": "aola_test"}
    response = requests.get(aola["url"], stream=True)
    filename = remove_unvalid_chars(aola["name"]) + ".jpg"
    with open(folder / filename, "wb") as f:
        shutil.copyfileobj(response.raw, f)
    print(f'{aola["name"]}.jpg is finished.')


def download_images(dir: str):
    folder = Path(dir).expanduser()
    if not folder.exists():
        folder.mkdir()
    # aola_img_test_url(folder)

    for i in get_image_urls():
    # for i in jenny_0():
        response = requests.get(i["url"], stream=True)
        filename = remove_unvalid_chars(i["name"]) + ".jpg"
        with open(folder / filename, "wb") as f:
            shutil.copyfileobj(response.raw, f)
        print(f'{i["name"]}.jpg is finished.')


if __name__ == "__main__":
    save_folder = r"~/Pictures/images"
    download_images(save_folder)
