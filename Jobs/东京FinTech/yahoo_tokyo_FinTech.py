import datetime
import re
import time

import pymysql
import requests
from lxml import etree
from requests.exceptions import RequestException

def call_page(url):
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


def remove_block(items):
    new_items = []
    for it in items:
        f = "".join(it.split())
        new_items.append(f)
    return new_items

# 正则和lxml混用
def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    selector = etree.HTML(html)
    try:

        job_name = selector.xpath('//*[@id="sr"]/div/div/h3/a/text()')
        f_jobname= remove_block(job_name)


        # 两种类型链接解析
        link = selector.xpath('//*[@id="sr"]/div/div/h3/a/@href')

        link_list = []
        for item in link:
            if item[0:4] == "http":
                link_list.append(item)
            else:

                f_item = 'https://job.yahoo.co.jp' + item
                link_list.append(f_item)

        type = selector.xpath('//*[@id="sr"]/div/div[2]/ul[1]/li[1]/text()')
        salary = selector.xpath('//*[@id="sr"]/div/div[2]/ul[1]/li[2]/text()')
        for i1,i2,i3,i4 in zip(salary,type,link_list,f_jobname):
            big_list.append((i1,i2,i3,i4))
        return big_list
    except  ValueError:
        pass




def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Yahoo_J',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into Tokyo_FinTech (salary,type,link,job_name) values (%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass



if __name__ == '__main__':
    for PageNum in range(1,101):
        url = 'https://job.yahoo.co.jp/jobs/?&keyword=FinTech&l=東京都&page='+str(PageNum)+'&ssid=f859a096-ced8-4e8b-be46-919495c19d70&comp=1'
        html = call_page(url)
        content = parse_html(html)
        insertDB(content)
        time.sleep(1)
        print(content)



# salary,type,link,job_name
# create table Tokyo_FinTech(
# id int not null primary key auto_increment,
# salary varchar(50),
# type varchar(28),
# link text,
# job_name text
# ) engine=InnoDB  charset=utf8;

# drop table Tokyo_openstack;

#







