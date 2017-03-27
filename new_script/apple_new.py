#!/usr/bin/env
# -*- coding: utf-8 -*-
__author__ = 'Vmture'

import time
from com.common import CommonFunction
from com.re_rules import apple_rules, message_kinds_apple

com = CommonFunction()
name = 'apple'

def get_update_messages():
    update_messages = [str(time.ctime())]
    datas = com.get_tmp_contents(name)
    update_data = ''
    for data in datas:
        if '更新日期' in data:
            update_data += data
    ####获取软件大小
    update_messages.append(com.re_find_messages(apple_rules['软件大小'], update_data))
    ####获取版本号
    update_messages.append(com.re_find_messages(apple_rules['版本号'], update_data))
    ####获取更新日期
    update_messages.append(com.re_find_messages(apple_rules['更新日期'], update_data))
    for data in datas:
        if '本次更新' in data:
            update_data += data
    ####获取本次更新
    update_messages.append(com.re_find_messages(apple_rules['本次更新'], update_data))
    ####获取近期更新
    update_messages.append(com.re_find_messages(apple_rules['近期更新'], update_data))
    return update_messages

def run():
    url = com.find_url(name)
    com.get_page_source_webdriver(url, name)
    last_messages = get_update_messages()
    path, end = com.run_a(name, last_messages, message_kinds_apple)
    return path, end

if __name__ == '__main__':
    path, end = run()
    print(path)
    print(end)