# getimg_zhihu.py
# Created : 17th April 2022
# Last modified : 17th April 2022
# Version : 1.0.3

'''
Description :

This script will get image from zhihu.
'''
# just checking
_author_ = "Winona"

from selenium import webdriver
import time
import re
import urllib.request
import pathlib

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://zhihu.com/question/357158101/answer/2412044724")
save_folder = r'~/Pictures/images'
i = 0

while i < 10:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    try:
        driver.find_element_by_css_selector('button.QuestionMainAction').click()
        print("page" + str(i))
        time.sleep(1)
    except:
        break
result_raw = driver.page_source
content_list = re.findall("img src=\"(.+?)\" ", str(result_raw))
n = 0

folder = pathlib.Path(save_folder).expanduser()
while n < len(content_list):
    i = time.time()
    local = (r"%s/%s.jpg" % (folder, i))
    urllib.request.urlretrieve(content_list[n], local)
    print("Number by time: " + str(i))
    n += 1
