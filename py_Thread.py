Thread 是threading模块中最重要的类之一，可以使用它来创建线程。有两种方式来创建线程：一种是通过继承Thread类，重写它的run方法；另一种是创建一个threading.Thread对象，在它的初始化函数（__init__）中将可调用对象作为参数传入

// 开启锁

self.lock.acquire()  

// 释放锁

self.lock.release()

定义一个锁,并不是给资源加锁,你可以定义多个锁,像下两行代码,当你需要占用这个资源时，任何一个锁都可以锁这个资源.

以下例子通过过线程获取url内容，在根据xpath获取对应的title

#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import threading
import Queue
import urllib2
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')

class ThreadUrl(threading.Thread):  
    def __init__(self,lock, queue):  
        super(ThreadUrl, self).__init__()
        self.lock = lock 
        self.queue = queue  

    def run(self):  
        while True:
            print self.getName()
            url = self.queue.get()  
            try:
                html=urllib2.urlopen(url, timeout=10).read()
                selector=etree.HTML(u'%s' % html, parser=None, base_url=None)
                title=selector.xpath("////h1[@class='rztpl-tit']/text()")[1]
                print title
            except:
                print url,'获取错误.'

            ''' 开启锁'''
            #self.lock.acquire()
            ''' 释放锁 '''
            #self.lock.release()
            ''' 结束 '''
            self.queue.task_done()  
  
if __name__ == "__main__":  
    urls=[
        'http://www.hrloo.com/rz/14105768.html',
        'http://www.hrloo.com/rz/14153682.html',
        'http://www.hrloo.com/rz/14153016.html',
        'http://www.hrloo.com/rz/14153042.html',
        'http://www.hrloo.com/rz/14105528.html'
        ]

    lock = threading.Lock()
    queue = Queue.Queue()
    for row in urls:
        t = ThreadUrl(lock, queue)
        t.setDaemon(True)
        t.start()

    for row in urls:
        queue.put(row)
    queue.join()


# 线程限制
def process_queue(process, end):
    s=1
    e=process
    for row in range(1, end):
        if s==1:
            print '{} {}'.format(1, process)
            s=e
            e=e+process
        else:
            print '{} {}'.format(s, e)
            s=e
            e=e+process
        time.sleep(1)
        
        
[root@NGphpMysql three]# python2.7 2.py 
职场微语录五！											
明明有好机会，为什么我不举荐你？											
哪有什么顺其自然，不过是自己逼自己（七）											
有没有一样东西，是你一定要得到的？											
招聘人才的核心——用“心”招		
