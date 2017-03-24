#!/usr/bin/env
# -*- coding: utf-8 -*-
__author__ = 'Vmture'

from selenium import webdriver
import re
import os
import codecs
import csv
from create_folders import create_folders
import time

appstore_tmp = '/tmp/tmp_appstore.txt'

with open('./urls.json', 'r') as urls:
    appstore_url = eval(urls.read())['apple_store']


def get_page_source():
    driver = webdriver.PhantomJS(executable_path='./phantomjs')
    driver.get(appstore_url.encode('utf8'))
    page_source = driver.page_source
    driver.close()
    with open(appstore_tmp, 'wb') as F:
        F.write(page_source.encode('utf8'))

def create_csv(appstore_path):
    path = os.listdir(appstore_path)
    message_kinds = ['查询时间', '软件大小', '版本号', '更新时间', '本次更新', '近期更新']
    if 'apple.csv' not in path:
        with open(appstore_path+'/apple.csv', 'wb') as F:
            F.write(codecs.BOM_UTF8)
            csv_writer = csv.writer(F, dialect='excel')
            csv_writer.writerow(message_kinds)

def get_update_messages_a():
    update_messages = [str(time.ctime())]
    with open(appstore_tmp, 'r') as F:
        datas = F.readlines()
    update_data = ''
    for data in datas:
        if '更新日期' in data:
            update_data += data
    ####获取软件大小
    if re.compile(r'<li><span class="label">大小： </span>([\d\.]+ MB)</li><li><span class="label">Apple').findall(update_data):
        update_messages.append(re.compile(r'<li><span class="label">大小： </span>([\d\.]+ MB)</li><li><span class="label">Apple').findall(update_data)[0])
    ####获取版本号
    if re.compile(r'<span itemprop="softwareVersion">(.+)</span></li><li><span class="label">').findall(update_data):
        update_messages.append(re.compile(r'<span itemprop="softwareVersion">(.+)</span></li><li><span class="label">').findall(update_data)[0])
    ####获取更新日期
    if re.compile(r'Etc/GMT">(.+)</span></li><li><span class="label">版本:').findall(update_data):
        update_messages.append(re.compile(r'Etc/GMT">(.+)</span></li><li><span class="label">版本:').findall(update_data)[0])
    return update_messages

def get_update_messages_b(update_messages):
    with open(appstore_tmp, 'r') as F:
        datas = F.readlines()
    update_data = ''
    for data in datas:
        if '本次更新' in data:
            update_data += data
    ####获取本次更新
    if re.compile(r'>本次更新<br>-([\x80-\xff]+)；<br>近期更新').findall(update_data):
        update_messages.append(re.compile(r'>本次更新<br>-([\x80-\xff]+)；<br>近期更新').findall(update_data)[0])
    ####获取近期更新
    if re.compile(r'近期更新<br>-(.+)；</p>').findall(update_data):
        update_messages.append(re.compile(r'近期更新<br>-(.+)；</p>').findall(update_data)[0])
    return update_messages

def insert_data(base_messages, appstore_path):
    old_datas = list(csv.reader(open(appstore_path+'/apple.csv', 'r')))
    if old_datas[-1][2] != base_messages[2]:
    #根据版本号判断(旧数据最后的版本号与查询时的版本号)
        with open(appstore_path+'/apple.csv', 'wb') as F:
            F.write(codecs.BOM_UTF8)
            csv_writer = csv.writer(F, dialect='excel')
            for contents in old_datas:
                csv_writer.writerow(contents)
            csv_writer.writerow(base_messages)

def run():
    article_path = create_folders()
    appstore_path = article_path + r'/appstore'
    try:
        get_page_source()
        create_csv(appstore_path)
        update_messages = get_update_messages_a()
        messages = get_update_messages_b(update_messages)
        insert_data(messages, appstore_path)
        os.remove(appstore_tmp)
        file_path = appstore_path+'/apple.csv'
    except:
        file_path = '可能网络存在问题,请确定网络稳定的情况下再试.'
    return file_path


if __name__ == '__main__':
    run()
