# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import random
from datetime import date
import os
import threading
import sys,re

headers = {
        "Referer":"http://www.baidu.com/",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537."
    }

def get_pic(s, url, path):
    picname = url.split('/')
    picpath = path + '/' + str(picname[-1])
    print("picpath %s" % picpath)
    with open(picpath, 'wb') as fp:
        try:
            rep = s.get(url, headers = headers, timeout = 60, stream = True)
            for data in rep.iter_content(chunk_size = 512):
                fp.write(data)
            rep.close()
        except:
            print("%4s" % sys.exc_info());

def fetch_pic_list(url):
    rep = requests.get(url)
    rep.encoding='gb2312'
    soup = BeautifulSoup(rep.text, 'html5lib')
    dir = soup.find('div', class_ = 'content').h5.string
    pages = soup.find('div', class_ = 'content-page').span.string
    cnt = re.findall(r'\d+', pages)
    imgStr = soup.find('div',class_='content-pic').img['src']
    prefix = imgStr[:imgStr.rfind("/") + 1]
    picext = "." + imgStr.split(".")[-1]
    rep.close()
    piclist = [prefix + str(i + 1) + picext for i in range(int(cnt[0]))]
    return piclist, dir

def fetch_photo_list(url):
    resp = requests.get(url)
    resp.encoding = 'gb2312'
    soup = BeautifulSoup(resp.text, 'html5lib')
    name = soup.find('dl', class_ = 'list-left public-box').find_all('a')
    pattern = r'<a.*?href="http://([^"]*?).html".*?>.*?</a>'
    phlist = []
    for i in name:
        try:
            link = re.search(pattern, str(i))
            if link:
                for x in link.groups(): phlist.append("http://" + x + ".html")
        except TypeError:
            pass
    return phlist

def thief_run(url, path):
    s = requests.Session()
    phlist = fetch_photo_list(url)
    for ph in phlist:
        print(ph)
        piclist, dir = fetch_pic_list(ph)
        try:
            os.mkdir(path + '/' + dir)
        except:
            pass
        for pic in piclist:
            print("%4s" % pic)
            get_pic(s, pic, path + '/' + dir)
    s.close()

if __name__ == '__main__':
    if len(sys.argv) != 3 :
        print("Don't forget URL and Path")
        sys.exit()
    url = sys.argv[1]
    path = sys.argv[2]
    t = threading.Thread(target = thief_run, args = (url, path))
    t.start()
