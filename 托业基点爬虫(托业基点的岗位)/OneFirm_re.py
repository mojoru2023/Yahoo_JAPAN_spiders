import datetime
import re
import time

import pymysql
import requests
from lxml import etree
from requests.exceptions import RequestException

from selenium import webdriver

# def retry(times):
#     def wrapper(func):
#         def inner_wrapper(*args, **kwargs):
#             i = 0
#             while i < times:
#                 try:
#                     print(i)
#                     return func(*args, **kwargs)
#                 except:
#
#                     print("logdebug: {}()".format(func.__name__))
#                     i += 1
#
#         return inner_wrapper
#
#     return wrapper


# #
# @retry(2)	#	重试的次数 3





def call_page(url):
    # options = webdriver.ChromeOptions()
    # options.add_argument("--no-sandbox")
    # driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)
    # driver.get(url)
    # html = driver.page_source
    # return html
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None











def find_longest_str(str_list):
    '''
    找到列表中字符串最长的位置索引
    先获取列表中每个字符串的长度，查找长度最大位置的索引值即可
    '''
    num_list = [len(one) for one in str_list]
    index_num = num_list.index(max(num_list))
    return str_list[int(index_num)]


# 正则和lxml混用
def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    try:

        patt = re.compile(r"TOEIC\s*\d+", re.S)
        items = re.findall(patt, html)
        if len(items) !=0:

            f_item = find_longest_str(items)
            big_list.append(f_item)
        else:
            print("no toeic~~")
    except:
        pass










def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Yahoo_J',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into OneFirm_toeic (Firm_toeic,link) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass


if __name__ == '__main__':
    # 使用cursor()方法获取操作游标
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Yahoo_J',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cur = connection.cursor()
    #sql 语句
    for i in range(1,1960):
        sql = 'select * from allFirm_toeic where id = %s ' % i
        # #执行sql语句
        cur.execute(sql)
        # #获取所有记录列表
        data = cur.fetchone()
        url_str = data['link']


        html = call_page(url_str)
        try:
            big_list =[]
            content = parse_html(html)

            print(content,url_str)


            print(datetime.datetime.now())
            time.sleep(1)
        except ValueError :
            pass




# create table OneFirm_toeic(
# id int not null primary key auto_increment,
# Firm_toeic varchar(20),
# link text
# ) engine=InnoDB  charset=utf8;
#
# drop table OneFirm_toeic;


