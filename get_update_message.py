#!/usr/bin/env
# -*- coding: utf-8 -*-
__author__ = 'Vmture'
import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib

with open('./urls.json', 'r') as urls:
    shop_urls = eval(urls.read())

with open('./cookies.json', 'r') as cookies:
    xiaomi_cookies = eval(cookies.read())

def get_xiaomi_message():
    datas = {
        'id': 'com.ss.android.article.news',
        'ref': 'search',
    }
    header_datas = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'app.mi.com',
        'Referer': 'http://app.mi.com/search?keywords=%E4%BB%8A%E6%97%A5%E5%A4%B4%E6%9D%A1',
        'Upgrade-Insecure-Requests' :'1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
    }
    officialHeader = {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)',
        'referer': 'http://app1.sfda.gov.cn/datasearch/face3/dir.html',
        'Upgrade-Insecure-Requests': '1'
    }
    cookies_datas = {
        'xmuuid': 'XMGUEST-AE243880-02F2-11E7-ACA8-BF9307184AB7',
        'lastsource': 'www.baidu.com',
        'mstz': '||799177517.4||https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dgfi_qroqgs0cka4b_rnst3il8lxaq47u0ipwgdmsa1a%7Cwd%3D%7Ceqid%3Da9a79a98005451890000000458be3e07|',
        'mstuid': '1488862698751_883',
        'xm_vistor': '1488862698751_883_1488862698751-1488862698893',
        'JSESSIONID': 'aaaD0jArwy-Erfl1vrIOv',
        '__utma': '127562001.152940027.1488862717.1488862717.1488862717.1',
        '__utmc': '127562001',
        '__utmz': '127562001.1488862717.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=%E5%B0%8F%E7%B1%B3',
        '__utmb': '127562001.1.10.1488937803',
    }
    data = requests.get(shop_urls['xiaomi_url'], headers=header_datas, cookies=cookies_datas, timeout=10.0)
    time.sleep(1)
    print(data.content)
    print(data.encoding)
    print data.request
    data.close()

if __name__ == '__main__':
    get_xiaomi_message()