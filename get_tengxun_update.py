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

tengxun_tmp = '/tmp/tmp_tengxun.txt'

with open('./headers.json', 'r') as urls:
    tengxun_headers = eval(urls.read())['tengxun']

with open('./urls.json', 'r') as urls:
    tengxun_url = eval(urls.read())['tengxun_url']

def get_page_source():
    page_request = requests.get(tengxun_url, headers=tengxun_headers, timeout=10.0)
    page_source = page_request.content
    page_request.close()
    with open(tengxun_tmp, 'wb') as F:
        F.write(page_source)

def create_csv(tengxun_path):
    path = os.listdir(tengxun_path)
    message_kinds = ['查询时间', '软件大小', '版本号', '更新时间', '包名', 'appid', '更新内容']
    if 'tengxun.csv' not in path:
        with open(tengxun_path+'/tengxun.csv', 'wb') as F:
            F.write(codecs.BOM_UTF8)
            csv_writer = csv.writer(F, dialect='excel')
            csv_writer.writerow(message_kinds)

def get_update_messages_a():
    update_messages = [str(time.ctime())]
    with open(tengxun_tmp, 'r') as F:
        datas = F.readlines()
    for data in datas:
        ####获取软件大小
        if 'det-size' in data:
            update_messages.append(re.compile(r'\d+\.\d+M').findall(data)[0])
        ####获取版本号
        if 'det-othinfo-data' in data:
            if re.compile(r'>([\d\.V]+)<').findall(data):
                update_messages.append(re.compile(r'>([\d\.V]+)<').findall(data)[0])
        ####获取更新时间
        if 'J_ApkPublishTime' in data:
            update_time_a = re.compile(r'data-apkPublishTime="(\d+)"').findall(data)[0]
            update_time_b = time.strftime('%Y-%m-%d', time.localtime(int(update_time_a)))
            update_messages.append(update_time_b)
        ####获取下载地址
        if 'downUrl' in data:
            download_url = re.compile(r'"(.+)"').findall(data)[0]
    return update_messages, download_url

def get_update_messages_b(update_messages):
    with open(tengxun_tmp, 'r') as a:
        datas = a.readlines()
    numbers_a = []
    numbers_b = []
    update_datas = ''
    for data in datas:
        if 'var appDetailData = {' in data:
            numbers_a.append(datas.index(data))
    for number in xrange(numbers_a[0], len(datas)):
        if '}' in datas[number]:
            numbers_a.append(number)
    for number in xrange(numbers_a[0]+1, numbers_a[1]):
        ####获取包名
        if 'apkName' in datas[number]:
            update_messages.append(re.compile(r'"(.+)"').findall(datas[number])[0])
        ####获取appid
        if 'appId' in datas[number]:
            update_messages.append(re.compile(r'\d+').findall(datas[number])[0])
    ####获取更新内容
    for data in datas:
        if 'det-app-data-info' in data:
            numbers_b.append(datas.index(data))
    for number in xrange(numbers_b[0], numbers_b[1]+1):
        if '更新内容' in datas[number]:
            update_datas_list = re.compile(r'[\x80-\xff]+').findall(datas[number+1])
    for update_data in update_datas_list:
        update_datas += update_data
    update_messages.append(update_datas)
    return update_messages

def insert_data(base_messages, tengxun_path):
    old_datas = list(csv.reader(open(tengxun_path+'/tengxun.csv', 'r')))
    level_number = base_messages[2]
    apk_name = base_messages[4]+'_'+level_number+'.apk'
    if old_datas[-1][2] != base_messages[2]:
    #根据版本号判断(旧数据最后的版本号与查询时的版本号)
        with open(tengxun_path+'/tengxun.csv', 'wb') as F:
            F.write(codecs.BOM_UTF8)
            csv_writer = csv.writer(F, dialect='excel')
            for contents in old_datas:
                csv_writer.writerow(contents)
            csv_writer.writerow(base_messages)
    return apk_name

def run():
    article_path = create_folders()
    tengxun_path = article_path + r'/腾讯'
    try:
        get_page_source()
        create_csv(tengxun_path)
        update_messages, download_url = get_update_messages_a()
        messages = get_update_messages_b(update_messages)
        apk_name = insert_data(messages, tengxun_path)
        download_apk(tengxun_path, apk_name, download_url)
        os.remove(tengxun_tmp)
        file_path = tengxun_path+'/tengxun.csv'
    except:
        file_path = '可能网络存在问题,请确定网络稳定的情况下再试.'
    return file_path



if __name__ == '__main__':
    run()