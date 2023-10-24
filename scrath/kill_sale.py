import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def main():
    times = "2023-09-26 19:50:30"
    browser = webdriver.Chrome()
    browser.get("https://www.jd.com/")
    time.sleep(3)
    browser.find_element(By.LINK_TEXT, "你好，请登录").click()
    time.sleep(8)
    browser.get("https://cart.jd.com/cart_index")
    time.sleep(5)
    while True:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        if now > times:
            while True:
                try:
                    if browser.find_element(By.LINK_TEXT, ""):
                        browser.find_element(By.LINK_TEXT, "").click()
                        print("trying...")
                        break
                except:
                    pass
            while True:
                try:
                    if browser.find_element(By.LINK_TEXT, ""):
                        browser.find_element(By.LINK_TEXT, "").click()
                except:
                    print("you have an order waiting for payment")
                    break


if __name__ == "__main__":
    main()
