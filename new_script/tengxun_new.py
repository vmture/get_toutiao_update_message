#!/usr/bin/env
# -*- coding: utf-8 -*-
__author__ = 'Vmture'

from com.common import CommonFunction
from com.re_rules import tengxun_rules_a, tengxun_rules_b, message_kinds_tengxun
import time

com = CommonFunction()
name = '腾讯'

def get_update_messages():
    numbers_a = []
    numbers_b = []
    update_datas = ''
    update_messages = [str(time.ctime())]
    datas = com.get_tmp_contents(name)
    ####获取软件大小
    for data in datas:
        if tengxun_rules_a['软件大小'] in data:
            update_messages.append(com.re_find_messages(tengxun_rules_b['软件大小'], data))
            break
    ####获取版本号
    for data in datas:
        if tengxun_rules_a['版本号'] in data:
            update_messages.append(com.re_find_messages(tengxun_rules_b['版本号'], data))
            break
    ####获取更新时间
    for data in datas:
        if tengxun_rules_a['更新时间'] in data:
            update_messages.append(time.strftime('%Y-%m-%d', time.localtime(int(com.re_find_messages(tengxun_rules_b['更新时间'], data)))))
            break
    ####获取包名和appid
    for data in datas:
        if tengxun_rules_a['定位_a'] in data:
            numbers_a.append(datas.index(data))
    for number in xrange(numbers_a[0], len(datas)):
        if tengxun_rules_a['定位_b'] in datas[number]:
            numbers_a.append(number)
    for number in xrange(numbers_a[0]+1, numbers_a[1]):
        ####获取包名
        if tengxun_rules_a['包名'] in datas[number]:
            update_messages.append(com.re_find_messages(tengxun_rules_b['包名'], datas[number]))
        ####获取appid
        if tengxun_rules_a['appid'] in datas[number]:
            update_messages.append(com.re_find_messages(tengxun_rules_b['appid'], datas[number]))
    ####获取下载地址
    for data in datas:
        if tengxun_rules_a['下载地址'] in data:
            download_url = com.re_find_messages(tengxun_rules_b['下载地址'], data)
            break
    ####获取更新内容
    for data in datas:
        if tengxun_rules_a['更新内容'] in data:
            numbers_b.append(datas.index(data))
    for number in xrange(numbers_b[0], numbers_b[1]+1):
        if '更新内容' in datas[number]:
            update_datas_list = com.re_find_messages(tengxun_rules_b['更新内容'], datas[number+1])
    for update_data in update_datas_list:
        update_datas += update_data
    update_messages.append(update_datas)
    return update_messages, download_url

def run():
    url = com.find_url(name)
    header = com.find_header(name)
    com.get_page_source_requests(url, name, header)
    last_messages, download_url = get_update_messages()
    path, end = com.run_b(name, last_messages, download_url, message_kinds_tengxun)
    return path, end

if __name__ == '__main__':
    a, b = run()
    print(a)
    print(b)