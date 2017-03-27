#!/usr/bin/env
# -*- coding: utf-8 -*-
__author__ = 'Vmture'

from com.common import CommonFunction
from com.re_rules import baidu_rules_a, baidu_rules_b, message_kinds_baidu
import time
import re

com = CommonFunction()
name = '百度'

def get_update_messages():
    update_messages = [str(time.ctime())]
    datas = com.get_tmp_contents(name)
    ####获取软件大小
    for data in datas:
        if baidu_rules_a['软件大小'] in data:
            update_messages.append(com.re_find_messages(baidu_rules_b['软件大小'], data))
            break
    ####获取版本号
    for data in datas:
        if baidu_rules_a['版本号'] in data:
            update_messages.append(com.re_find_messages(baidu_rules_b['版本号'], data))
            break
    ####获取包名
    for data in datas:
        if baidu_rules_a['包名'] in data:
            update_messages.append(com.re_find_messages(baidu_rules_b['包名'], data))
            break
    ####获取下载地址
    for data in datas:
        if baidu_rules_a['下载地址'] in data:
            download_url = com.re_find_messages(baidu_rules_b['下载地址'], data)
            break
    ####获取应用介绍
    numbers = []
    for data in datas:
        if baidu_rules_a['应用介绍'] in data:
            numbers.append(datas.index(data))
    update_messages.append(re.compile(r'<br>').subn(' ', re.compile(baidu_rules_b['应用介绍']).findall(datas[numbers[-1]])[0])[0])
    return update_messages, download_url

def run():
    url = com.find_url(name)
    header = com.find_header(name)
    com.get_page_source_requests(url, name, header)
    last_messages, download_url = get_update_messages()
    path, end = com.run_b(name, last_messages, download_url, message_kinds_baidu)
    return path, end

if __name__ == '__main__':
    a, b = run()
    print(a)
    print(b)