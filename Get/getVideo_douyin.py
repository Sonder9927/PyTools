"""
the public：一行玩python
summary：
1.Crawl Douyin video
2.Asynchronous anti-crawlers
3.Parse the next page（max_cursor）
"""

import requests
import json
import os
import re
from icecream import ic


# download video
def down(name, url, dir_file):
    headers_down = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36',
    }
    r = requests.get(url, headers=headers_down)
    with open(dir_file + "/"+str(name) + ".mp4", 'wb+') as f:
        f.write(r.content)

# format title
def delete_boring_charaters(sentence):
    return re.sub('[0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "-", sentence)

# Get all videos under the homepage
def getlist(sec_id, dir_file):
    # id
    sec_uid = sec_id
    # Return number, the maximum is 34
    count = 34
    # next page
    max_cursor = 0
    # Determine if there is a next page
    has_more = True
    # Store video information
    videotitle_list = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0",
        "Accept": "application/json,text/javascript,*/*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip,deflate, br",
        "X-Requested-With": "XMLHttpRequest",
        'Access-Control-Allow-Origin': '*',
        "Connection": "keep-alive"
    }
    while (has_more):
        url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=" + str(sec_uid) + "&count=" + str(
            count) + "&max_cursor=" + str(max_cursor) + "&aid=1128&_signature=z1epBAAArxEnjYt5fPWXJs9XqR&dytk="
        r = requests.get(url, headers=headers)
        r.encoding = 'utf-8'
        da = json.loads(r.text)

        aweme_list = da['aweme_list']
        print(aweme_list)
        has_more = da['has_more']

        for i in aweme_list:
            title = delete_boring_charaters(i['desc'])
            video_url = i['video']['play_addr']['url_list'][0]
            videotitle_list.append(title)
            down(title, video_url, dir_file)
            print(title + "-Download completed!")

        videotitle_list = list(set(videotitle_list))
        print(len(videotitle_list))

        #if (len(videotitle_list) > 10):
        #    break

        if has_more:
            max_cursor = da['max_cursor']
        else:
            break

def get_douyin():
    # id
    #sec_id = "MS4wLjABAAAA8t3b1dsGNvJgc6cUe-Bm2JCyqtrs_c1zJZT6TmgxurkcAyap5aE-PRXpLX2tFuiu"
    sec_id = "MS4wLjABAAAA8O_5V9XFEAT2lVkyDsT4SgtslsvRehabDaSc5KRXevM"
    # directory for storage
    dir_file = "静静"
    # If the directory does not exist, create it
    if not os.path.exists(dir_file):
        os.mkdir(dir_file)

    getlist(sec_id, dir_file)

if __name__ == "__main__":
    get_douyin()
