

import datetime

import pymysql
import requests
from lxml import etree
import json
from queue import Queue
import threading
from requests.exceptions import RequestException




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



class QiubaiSpider(object):

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        }
        self.url_pattern = 'https://job.yahoo.co.jp/jobs/?&keyword=CFA&l=東京都&page={0}&ssid=25158ae9-0705-4dd3-85a3-30a1930eb123&comp=1'
        # url 队列
        self.url_queue = Queue()
        # 响应队列
        self.page_queue = Queue()
        # 数据队列
        self.data_queue = Queue()


    def add_url_to_queue(self):
        # 把URL添加url队列中
        for i in range(1,101):
            self.url_queue.put(self.url_pattern.format(i))

    @run_forever
    def add_page_to_queue(self):
        ''' 发送请求获取数据 '''
        url = self.url_queue.get()
        # print(url)
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            self.url_queue.put(url)
        else:
            self.page_queue.put(response.content)
        # 完成当前URL任务
        self.url_queue.task_done()

    @run_forever
    def add_dz_to_queue(self):
        '''根据页面内容使用lxml解析数据, 获取段子列表'''
        page = self.page_queue.get()

        big_list = []
        selector = etree.HTML(page)
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
        except  ValueError:
            pass





        self.data_queue.put(big_list)
        self.page_queue.task_done()



    @run_forever
    def insertDB(self):

        dz_list = self.data_queue.get()


        connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Yahoo_J',
                                    charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

        cursor = connection.cursor()
        try:
            cursor.executemany('insert into Tokyo_CFA (salary,type,link,job_name) values (%s,%s,%s,%s)', dz_list)
            connection.commit()
            connection.close()
            print('向MySQL中添加数据成功！')
        except TypeError :
            pass
        self.data_queue.task_done()


    def run_use_more_task(self, func, count=1):
        '''把func放到线程中执行, count:开启多少线程执行'''
        for i in range(0, count):
            t = threading.Thread(target=func)
            t.setDaemon(True)
            t.start()

    def run(self):
        # 开启线程执行上面的几个方法
        url_t = threading.Thread(target=self.add_url_to_queue)
        # url_t.setDaemon(True)
        url_t.start()

        self.run_use_more_task(self.add_page_to_queue,4)
        self.run_use_more_task(self.add_dz_to_queue, 3)
        self.run_use_more_task(self.insertDB, 2)


        # 使用队列join方法,等待队列任务都完成了才结束
        self.url_queue.join()
        self.page_queue.join()
        self.data_queue.join()







if __name__ == '__main__':
    print(datetime.datetime.now())
    s = datetime.datetime.now()



    qbs = QiubaiSpider()
    qbs.run()

    print(datetime.datetime.now())

    e = datetime.datetime.now()
    f = e-s
    print(f)






