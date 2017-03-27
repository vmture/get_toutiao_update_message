#!/usr/bin/env
# -*- coding: utf-8 -*-
__author__ = 'Vmture'

from com.common import CommonFunction
from com.re_rules import xiaomi_rules, message_kinds_xiaomi
import time
import re

com = CommonFunction()
name = '小米'

def get_update_messages():
    update_datas = ''
    update_messages = [str(time.ctime())]
    datas = com.get_tmp_contents(name)
    ####获取定位内容
    for data in datas:
        if re.compile(xiaomi_rules['定位_a']).search(data):
            contents_a = com.re_find_messages(xiaomi_rules['定位_a'], data)
            number = datas.index(data)
        if re.compile(xiaomi_rules['定位_b']).search(data):
            contents_b = com.re_find_messages(xiaomi_rules['定位_b'], data)
    ####获取软件大小
    update_messages.append(com.re_find_messages(xiaomi_rules['软件大小'], contents_a))
    ####获取版本号
    update_messages.append(com.re_find_messages(xiaomi_rules['版本号'], contents_a))
    ####获取更新时间
    update_messages.append(com.re_find_messages(xiaomi_rules['更新时间'], contents_a))
    ####获取包名
    update_messages.append(com.re_find_messages(xiaomi_rules['包名'], contents_a))
    ####获取appid
    update_messages.append(com.re_find_messages(xiaomi_rules['appid'], contents_a))
    ####获取下载地址
    download_url = 'http://app.mi.com' + com.re_find_messages(xiaomi_rules['下载地址'], datas[number])
    ####获取更新内容
    update_datas_list = re.compile(xiaomi_rules['新版特性']).findall(contents_b)
    for data in update_datas_list[1:]:
        update_datas += data+'; '
    update_messages.append(update_datas)
    return update_messages, download_url

def run():
    url = com.find_url(name)
    header = com.find_header(name)
    com.get_page_source_requests(url, name, header)
    last_messages, download_url = get_update_messages()
    path, end = com.run_b(name, last_messages, download_url, message_kinds_xiaomi)
    return path, end

if __name__ == '__main__':
    a, b = run()
    print(a)
    print(b)