#! -*- coding:utf-8 -*-
import datetime
import re
import time

import pymysql
import requests
from lxml import etree
from selenium import webdriver

driver = webdriver.Chrome()
# 把find_elements 改为　find_element
def get_first_page():

    url = 'https://job.yahoo.co.jp/jobs/python%E9%96%A2%E9%80%A3%E3%81%AE%E6%B1%82%E4%BA%BA-%E6%9D%B1%E4%BA%AC%E9%83%BD'
    driver.get(url)



    html = driver.page_source
    return html



# 把首页和翻页处理？

def next_page():
    for i in range(1,101):  # selenium 循环翻页成功！
        driver.find_element_by_xpath('//*[@id="Sp1"]/div/ol/li[last()]/a').click()
        time.sleep(1)
        html = driver.page_source
        return html



def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    selector = etree.HTML(html)
    job_name = selector.xpath('//*[@id="sr"]/div/div/h3/a/text()')

    link = selector.xpath('//*[@id="sr"]/div/div/h3/a/@href')

    info1 = selector.xpath('//*[@id="sr"]/div/ul/li[1]/text()')

    short_info = selector.xpath('//*[@id="sr"]/div/p[1]/text()')
    patt = re.compile('<p class="resultItem__src">(.*?)</p>',re.S) #使用正则吧
    info_froms = re.findall(patt,html)

    long_tuple = (i for i in zip(job_name, link, info1,short_info,info_froms))
    for i in long_tuple:
        big_list.append(i)
    return big_list


        # 存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456',
                                 db='Yahoo_J',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into yahoo_python_jobs (job_name,link,info1,short_info,info_from) values (%s,%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration:
        pass



#
if __name__ == '__main__':
        html = get_first_page()
        content = parse_html(html)
        time.sleep(1)
        insertDB(content)
        while True:
            html = next_page()
            content = parse_html(html)
            insertDB(content)
            print(datetime.datetime.now())
            time.sleep(1)
#

# # #
# create table yahoo_python_jobs(
# id int not null primary key auto_increment,
# job_name text,
# link text,
# info1 varchar(50),
# short_info varchar(80),
# info_from text
# ) engine=InnoDB  charset=utf8;
#
#
#
# drop table yahoo_python_jobs;
#

