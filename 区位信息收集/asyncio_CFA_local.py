

import datetime

import pymysql
import requests
from lxml import etree
import json
from queue import Queue
import threading
from requests.exceptions import RequestException






import asyncio
import aiohttp


def run_forever(func):
    def wrapper(obj):
        while True:
            func(obj)
    return wrapper

def find_longest_str(str_list):
    '''
    找到列表中字符串最长的位置索引
    先获取列表中每个字符串的长度，查找长度最大位置的索引值即可
    '''
    num_list = [len(one) for one in str_list]
    index_num = num_list.index(max(num_list))
    return str_list[int(index_num)]


def remove_block(items):
    new_items = []
    for it in items:
        f = "".join(it.split())
        new_items.append(f)
    return new_items



async def get_title(i):


    url = 'https://job.yahoo.co.jp/jobs/?&keyword=CFA&l=東京都&page={0}&ssid=25158ae9-0705-4dd3-85a3-30a1930eb123&comp=1'.format(i)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(resp.status)
            text = await resp.text()
            print('start', i)

    big_list = []
    selector = etree.HTML(text)



    # 两种类型链接解析
    location_info = selector.xpath('//*[@id="sr"]/div/div[2]/ul[1]/li[3]/text()')
    for item in location_info:



        big_list.append((item))


    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Yahoo_J',charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into Tokyo_CFA_locInfo (lcinfo) values (%s)', big_list)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass






loop = asyncio.get_event_loop()
fun_list = (get_title(i) for i in range(1,101))
loop.run_until_complete(asyncio.gather(*fun_list))


# salary,type,link,job_name
# create table Tokyo_CFA_locInfo(
# id int not null primary key auto_increment,
# lcinfo varchar(50)
# ) engine=InnoDB  charset=utf8;