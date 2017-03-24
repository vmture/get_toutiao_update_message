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

qihu_tmp = '/tmp/tmp_360.txt'

with open('./urls.json', 'r') as urls:
    qiku_url = eval(urls.read())['360_url']

def get_page_source():
    page_request = requests.get(qiku_url, timeout=10.0)
    page_source = page_request.content
    page_request.close()
    with open(qihu_tmp, 'wb') as F:
        F.write(page_source)

def create_csv(qihu_path):
    path = os.listdir(qihu_path)
    message_kinds = ['查询时间', '软件大小', '版本号', '更新时间', '包名', '更新内容']
    if '360.csv' not in path:
        with open(qihu_path+'/360.csv', 'wb') as F:
            F.write(codecs.BOM_UTF8)
            csv_writer = csv.writer(F, dialect='excel')
            csv_writer.writerow(message_kinds)

def get_update_messages_a():
    update_messages = [str(time.ctime())]
    with open(qihu_tmp, 'r') as F:
        datas = F.readlines()
        ####获取软件大小
    for data in datas:
        if 'class="s-3"' in data:
            if re.compile(r'\d+\.\d+M').findall(data):
                update_messages.append(re.compile(r'\d+\.\d+M').findall(data)[0])
        ####获取版本号
    for data in datas:
        if '版本：' in data:
            if re.compile(r'>([\d\.V]+)<').findall(data):
                update_messages.append(re.compile(r'>([\d\.V]+)<').findall(data)[0])
        ####获取更新时间
    for data in datas:
        if '更新时间：' in data:
            if re.compile(r'>([\d\-]+)<').findall(data):
                update_messages.append(re.compile(r'>([\d\-]+)<').findall(data)[0])
        ####获取包名
    for data in datas:
        if 'pname' in data:
            if re.compile(r'"(.+)"').findall(data):
                update_messages.append(re.compile(r'"(.+)"').findall(data)[0])
        ####获取下载地址
    for data in datas:
        if 'downloadUrl' in data:
            download_url = re.compile(r"http.+apk").findall(data)[0]
    return update_messages, download_url

def get_update_messages_b(update_messages):
    with open(qihu_tmp, 'r') as F:
        datas = F.readlines()
    numbers = []
    update_datas = ''
    for data in datas:
        if '更新内容' in data:
            numbers.append(datas.index(data))
        if 'brief-toggle' in data:
            numbers.append(datas.index(data))
    for number in xrange(numbers[0], numbers[1]):
        if re.compile(r'[\x80-\xff]+').findall(datas[number]):
            update_datas_list = re.compile(r'[\x80-\xff]+').findall(datas[number])
            for update_data in update_datas_list:
                if '更新内容' not in update_data :
                    update_datas += update_data+';'
    update_messages.append(update_datas)
    return update_messages

def insert_data(base_messages, qihu_path):
    old_datas = list(csv.reader(open(qihu_path+'/360.csv', 'r')))
    level_number = base_messages[2]
    apk_name = base_messages[4]+'_'+level_number+'.apk'
    if old_datas[-1][2] != base_messages[2]:
    #根据版本号判断(旧数据最后的版本号与查询时的版本号)
        with open(qihu_path+'/360.csv', 'wb') as F:
            F.write(codecs.BOM_UTF8)
            csv_writer = csv.writer(F, dialect='excel')
            for contents in old_datas:
                csv_writer.writerow(contents)
            csv_writer.writerow(base_messages)
    return apk_name

def run():
    article_path = create_folders()
    qihu_path = article_path + r'/360'
    try:
        get_page_source()
        create_csv(qihu_path)
        update_messages, download_url = get_update_messages_a()
        messages = get_update_messages_b(update_messages)
        apk_name = insert_data(messages, qihu_path)
        download_apk(qihu_path, apk_name, download_url)
        os.remove(qihu_tmp)
        file_path = qihu_path+'/360.csv'
    except:
        file_path = '可能网络存在问题,请确定网络稳定的情况下再试.'
    return file_path

if __name__ == '__main__':
    run()