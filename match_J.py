# -*- coding:utf-8 -*-
import datetime
import re
import time

import pymysql

from lxml import etree
from selenium import webdriver

driver = webdriver.Chrome()


def get_first_page(url):

    driver.get(url)
    driver.find_element_by_xpath('//*[@id="mainContent"]/section/form/div/div/div/div[2]/div/label/span/span').send_keys("291109028@qq.com") #用户名
    driver.find_element_by_xpath('//*[@id="mainContent"]/section/form/div/div/div/div[3]/div/label/span/span').send_keys("mingyifan2007")#密码
    driver.find_element_by_xpath('//*[@id="mainContent"]/section/form/div/div/div/div[4]/button').click()
    time.sleep(3)


    html = driver.page_source
    return html


url = 'https://jp.match.com/login'

html = get_first_page(url)
print(html)