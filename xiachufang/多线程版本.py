# coding:utf-8
import os
import threading
from queue import Queue
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


# 初始化一些全局参数
img_queue = Queue() # 存放 img tag
threads = [] # 线程池
threads_num = 5 # 线程数
# 初始化下载文件目录
image_dir = os.path.join(os.curdir, 'images')
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

def HtmlDownload(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers)
    except Exception as e:
        print('出错了：', e)
        return
    else:
        r.encoding='utf-8'
        return r.text

def HtmlParser(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for img in soup.select('img'):
        if img.has_attr('data-src'):
            img_queue.put(img['data-src'])

def DataOutput(img):
        o = urlparse(img)
        filename = o.path[1:].split('@')[0]
        filepath = os.path.join(image_dir, filename)
        url = '%s://%s/%s' % (o.scheme, o.netloc, filename)
        print(url)  # https://i2.chuimg.com//33aaefd6b4ce4f719f88c97e08debd82_1080w_741h.jpg
        try:
            req = requests.get(url)
        except Exception as e:
            print('出错了：', e)
        else:
            with open(filepath, 'wb') as f:
                for chunk in req.iter_content(5050):
                    f.write(chunk)


def download():
    while True:
        # 阻塞直到从队列中获得一条消息
        img = img_queue.get()
        if img is None:
            break
        DataOutput(img)
        img_queue.task_done() #  向队列发送任务已经完成的信号， 必要的  否则线程将一直挂起
        # 队列还剩余多少
        print('remaining queue %s' % img_queue.qsize())

def crawler(root_url):
    html_content = HtmlDownload(root_url)
    img_list = HtmlParser(html_content)

    # 建立 5 个线程
    for i in range(threads_num):
        t = threading.Thread(target=download(), name='ImgDownload'+str(i))
        threads.append(t)
        t.start()
    #阻塞队列，直到队列被清空
    img_queue.join() # 等待队列为空
    # 向队列发送None以通知线程退出
    for i in range(threads_num):
        img_queue.put(None)
    # 退出线程
    for t in threads:
        t.join()
    print('Finished!')

if __name__=='__main__':
    crawler("https://www.xiachufang.com")