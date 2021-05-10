# coding:utf-8
import os
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

r = requests.get('https://www.xiachufang.com', headers = headers)
soup = BeautifulSoup(r.text, 'html.parser')

img_list = []
for img in soup.select('img'):
    if img.has_attr('data-src'):
        img_list.append(img.attrs['data-src'])
        # print(img.attrs['data-src'])

# 初始化下载文件目录
image_dir = os.path.join(os.curdir, 'images')
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

for img in img_list:
    o = urlparse(img)
    # print(o)
    filename = o.path[1:].split('@')[0]
    filepath = os.path.join(image_dir, filename)
    url = '%s://%s/%s' % (o.scheme, o.netloc, filename)
    print(url)    # https://i2.chuimg.com//33aaefd6b4ce4f719f88c97e08debd82_1080w_741h.jpg
    req = requests.get(url)
    with open(filepath, 'wb') as f:
            for chunk in req.iter_content(2048):
                f.write(chunk)

print('爬取完毕！')