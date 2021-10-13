# coding = utf-8
import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.maximize_window()
browser.set_window_size(800, 1024)
browser.get("http://www.baidu.com")
time.sleep(1)
browser.find_element_by_xpath("//a[contains(text(),'新闻')]").click()#在a标签下有个文本
time.sleep(10)

if 0:
    browser.find_element_by_id("kw").send_keys("selenium")
    time.sleep(1)
    browser.find_element_by_id("su").click()
    time.sleep(10)
    browser.quit()