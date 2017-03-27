#!/usr/bin/env
# -*- coding: utf-8 -*-
__author__ = 'Vmture'
import requests
import re
import os
import codecs
import csv
from create_folders import create_folders
import time
from download_apk import download_apk

baidu_tmp = '/tmp/tmp_baidu.txt'

with open('./headers.json', 'r') as urls:
    baidu_headers = eval(urls.read())['baidu']

with open('./urls.json', 'r') as urls:
    baidu_url = eval(urls.read())['baidu_url']

def get_page_source():
    page_request = requests.get(baidu_url, headers=baidu_headers, timeout=10.0)
    page_source = page_request.content
    page_request.close()
    with open(baidu_tmp, 'wb') as F:
        F.write(page_source)


def create_csv(baidu_path):
    path = os.listdir(baidu_path)
    message_kinds = ['查询时间', '软件大小', '版本号', '包名', '应用介绍']
    if 'baidu.csv' not in path:
        with open(baidu_path+'/baidu.csv', 'wb') as F:
            F.write(codecs.BOM_UTF8)
            csv_writer = csv.writer(F, dialect='excel')
            csv_writer.writerow(message_kinds)

def get_update_messages_a():
    update_messages = [str(time.ctime())]
    with open(baidu_tmp, 'r') as F:
        datas = F.readlines()
    ####获取软件大小
    for data in datas:
        if 'class="size' in data:
            update_messages.append(re.compile(r'\d+\.\d+M').findall(data)[0])
            break
    ####获取版本号
    for data in datas:
        if 'class="version' in data:
            update_messages.append(re.compile(r'[\d\.]+').findall(data)[0])
            break
    ####获取包名
    for data in datas:
        if 'data_package' in data:
            update_messages.append(re.compile(r'"(.+)"').findall(data)[0])
            break
    ####获取下载地址
    for data in datas:
        if 'data_url' in data:
            download_url = re.compile(r'"(.+)"').findall(data)[0]
            break
    return update_messages, download_url

def get_update_messages_b(update_messages):
    with open(baidu_tmp, 'r') as F:
        datas = F.readlines()
    ####获取应用介绍
    numbers = []
    for data in datas:
        if 'content content_hover'in data:
            numbers.append(datas.index(data))
    update_messages.append(re.compile(r'<br>').subn(' ', re.compile(r'>(.+)<br>今日头条').findall(datas[numbers[-1]])[0])[0])
    return update_messages

def insert_data(base_messages, baidu_path):
    old_datas = list(csv.reader(open(baidu_path+'/baidu.csv', 'r')))
    level_number = base_messages[2]
    apk_name = base_messages[3]+'_'+level_number+'.apk'
    if old_datas[-1][2] != base_messages[2]:
    #根据版本号判断(旧数据最后的版本号与查询时的版本号)
        with open(baidu_path+'/baidu.csv', 'wb') as F:
            F.write(codecs.BOM_UTF8)
            csv_writer = csv.writer(F, dialect='excel')
            for contents in old_datas:
                csv_writer.writerow(contents)
            csv_writer.writerow(base_messages)
    return apk_name

def run():
    article_path = create_folders()
    baidu_path = article_path + r'/百度'
    try:
        get_page_source()
        create_csv(baidu_path)
        update_messages, download_url = get_update_messages_a()
        messages = get_update_messages_b(update_messages)
        apk_name = insert_data(messages, baidu_path)
        download_apk(baidu_path, apk_name, download_url)
        os.remove(baidu_tmp)
        file_path = baidu_path+'/baidu.csv'
    except:
        file_path = '可能网络存在问题,请确定网络稳定的情况下再试.'
    return file_path

if __name__ == '__main__':
    run()