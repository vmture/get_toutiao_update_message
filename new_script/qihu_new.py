#!/usr/bin/env
# -*- coding: utf-8 -*-
__author__ = 'Vmture'

from com.common import CommonFunction
from com.re_rules import qihu_rules_a, qihu_rules_b, message_kinds_360
import time
import re

com = CommonFunction()
name = '360'

def get_update_messages():
    numbers = []
    update_datas = ''
    update_messages = [str(time.ctime())]
    datas = com.get_tmp_contents(name)
    ####获取软件大小
    for data in datas:
        if qihu_rules_a['软件大小'] in data:
            if re.compile(qihu_rules_b['软件大小']).search(data):
                update_messages.append(com.re_find_messages(qihu_rules_b['软件大小'], data))
                break
    ####获取版本号
    for data in datas:
        if qihu_rules_a['版本号'] in data:
            update_messages.append(com.re_find_messages(qihu_rules_b['版本号'], data))
            break
    ####获取更新时间
    for data in datas:
        if qihu_rules_a['更新时间'] in data:
            update_messages.append(com.re_find_messages(qihu_rules_b['更新时间'], data))
            break
    ####获取包名
    for data in datas:
        if qihu_rules_a['包名'] in data:
            update_messages.append(com.re_find_messages(qihu_rules_b['包名'], data))
            break
    ####获取下载地址
    for data in datas:
        if qihu_rules_a['下载地址'] in data:
            download_url = com.re_find_messages(qihu_rules_b['下载地址'], data)
            break
    ####获取更新内容
    for data in datas:
        if qihu_rules_a['定位_a'] in data:
            numbers.append(datas.index(data))
        if qihu_rules_a['定位_b'] in data:
            numbers.append(datas.index(data))
    for number in xrange(numbers[0], numbers[1]):
        if re.compile(qihu_rules_b['更新内容']).search(datas[number]):
            update_datas_list = re.compile(qihu_rules_b['更新内容']).findall(datas[number])
            for update_data in update_datas_list:
                if qihu_rules_a['定位_a'] not in update_data :
                    update_datas += update_data+';'
    update_messages.append(update_datas)
    return update_messages, download_url

def run():
    url = com.find_url(name)
    header = com.find_header(name)
    com.get_page_source_requests(url, name, header)
    last_messages, download_url = get_update_messages()
    path, end = com.run_b(name, last_messages, download_url, message_kinds_360)
    return path, end

if __name__ == '__main__':
    a, b = run()
    print(a)
    print(b)