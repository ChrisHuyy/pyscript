import requests
from dao import *
from bs4 import BeautifulSoup
import gevent
import json
from gevent.queue import Queue
from gevent import monkey; monkey.patch_all()

monkey.patch_all()
hypstar_user_url = 'https://www.hypstar.com/share/load_videos/?offset=0&count=21&user_id={}'
products = Queue()

def req(name):
    while not products.empty():
        print products.qsize()
        uid = products.get_nowait()
        try:
            ret = requests.get(hypstar_user_url.format(uid),timeout=10)
        except:
            print name,'request fail'
            ret = None
        if ret:
            data = json.loads(ret.content)
            if data and data['data']:
                if data['data']['items'] and len(data['data']['items'])>0:
                    print name,' working...'
                    print 'file ok the program going on, uid is : ',uid
                    print 'data len :', len(data['data']['items'])
                else:
                    print name,' working...'
                    print 'Suspected: ',uid
        # soup = BeautifulSoup(ret.content,"lxml")
        # soup_video = soup.find('div',class_='video-list no-video')
        # if soup_video:
        #     print 'Suspected: ',uid
        # else:
        #     pass


def loader(min,max):
    QUERY = "SELECT `user_id` FROM `tb_ugc_user` WHERE `source` like '%hypstar%' AND `article` > 0 AND `status`<>2 AND `id` > {} AND `id` < {}".format(min,max)
    data_task = query_and_fetch_all(QUERY)
    if data_task:
        return data_task


def modify(uid):
    MODIFY = 'UPDATE `tb_ugc_user` SET `status` = 2 WHERE  `user_id` ={};'.format(uid)
    answer = execute(MODIFY)
    if answer:
        print 'modify user {}'.format(uid)

def producer():
    for i in range(18):
        min = i*30000
        max = (i+1)*30000
        tasks = loader(min,max)
        for task in tasks:
            products.put(task['user_id'])
            # req(task['user_id'])

def main():
    gevent.joinall([
        gevent.spawn(producer),
        gevent.spawn(req,'steve'),
        gevent.spawn(req,'john'),
        gevent.spawn(req,'nancy'),
        gevent.spawn(req,'Belle'),
        gevent.spawn(req,'Edwina'),
        gevent.spawn(req,'Jessica'),
        gevent.spawn(req,'Louise'),
        gevent.spawn(req,'Luke'),
        gevent.spawn(req,'Mars'),
        gevent.spawn(req,'Roger'),
        ])


if __name__ == '__main__':
    main()