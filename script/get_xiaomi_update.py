#!/usr/bin/env
# -*- coding: utf-8 -*-
__author__ = 'Vmture'
from selenium import webdriver
import re
import csv
import time
import os
import codecs
from create_folders import create_folders
from download_apk import download_apk

with open('./urls.json', 'r') as urls:
    xiaomi_url = eval(urls.read())['xiaomi_url']

xiaomi_tmp = '/tmp/tmp_xiaomi.txt'

def get_page_source():
    driver = webdriver.PhantomJS(executable_path='./phantomjs')
    driver.get(xiaomi_url)
    page_source = driver.page_source
    driver.quit()
    with open(xiaomi_tmp, 'wb') as tmp:
        tmp.write(page_source.encode('utf8'))

###拼接更新的csv内容
# def get_base_message(page_source):
def get_base_message(new_upgrate):
    new_contents = ''
    # base_message = re.compile(r'<ul class=" cf">(.+)</ul><div class="weight-font float-div">').findall(page_source)[0]
    with open(xiaomi_tmp, 'r') as f:
        F = f.read()
    base_message = re.compile(r'<ul class=" cf">(.+)</ul><div class="weight-font float-div">').findall(F)[0]
    base_message_a = base_message.split('><')
    base_messages = [str(time.ctime())]
    for message_num in range(len(base_message_a))[1::2]:
        base_messages.append(re.compile(r'>(.+)<').findall(base_message_a[message_num])[0])
    if len(new_upgrate) != 0:
        for new_content in new_upgrate:
            new_contents += new_content+'; '
    base_messages.append(new_contents)
    return base_messages

####获取更新信息
def get_update_data():
    numbers = []
    new_upgrate = []
    with open(xiaomi_tmp, 'r') as f:
        F = f.readlines()
    for data in F:
        if '</p><h3 class="special-h3' in data:
            numbers.append(F.index(data))
    ####获取本次更新内容
    for number in xrange(numbers[0], numbers[1]+1):
        if re.compile(r'[\x80-\xff]+').findall(F[number]):
            if number == numbers[0]:
                new_upgrate.append(re.compile(r'[\x80-\xff]+').findall(F[number])[-1])
            else:
                new_upgrate.append(re.compile(r'[\x80-\xff]+').findall(F[number])[0])
    return new_upgrate



def create_csv(xiaomi_path):
    path = os.listdir(xiaomi_path)
    message_kinds = ['查询时间', '软件大小', '版本号', '更新时间', '包名', 'appid', '新版特性']
    if 'xiaomi.csv' not in path:
        with open(xiaomi_path+'/xiaomi.csv', 'wb') as F:
            F.write(codecs.BOM_UTF8)
            csv_writer = csv.writer(F, dialect='excel')
            csv_writer.writerow(message_kinds)


def insert_data(base_messages, xiaomi_path):
    old_datas = list(csv.reader(open(xiaomi_path+'/xiaomi.csv', 'r')))
    level_number = base_messages[2]
    apk_name = base_messages[4]+'_'+level_number+'.apk'
    if old_datas[-1][2] != base_messages[2]:
    #根据版本号判断(旧数据最后的版本号与查询时的版本号)
        with open(xiaomi_path+'/xiaomi.csv', 'wb') as F:
            F.write(codecs.BOM_UTF8)
            csv_writer = csv.writer(F, dialect='excel')
            for contents in old_datas:
                csv_writer.writerow(contents)
            csv_writer.writerow(base_messages)
    return apk_name

def get_download_url():
    with open(xiaomi_tmp, 'r') as tmp:
        tmps = tmp.readlines()
    for line in tmps:
        if '直接下载' in line:
            datas_a = line.split('><')
    for line in datas_a :
        if '直接下载' in line:
            datas_b = line
    download_path = re.compile(r'a href="(.+)" class="download"').findall(datas_b)[0]
    download_url = 'http://app.mi.com' + download_path
    return download_url


def run():
    article_path = create_folders()
    xiaomi_path = article_path+r'/小米'
    try:
        get_page_source()
        create_csv(xiaomi_path)
        new = get_update_data()
        messages = get_base_message(new)
        apk_name = insert_data(messages, xiaomi_path)
        download_url = get_download_url()
        download_apk(xiaomi_path, apk_name, download_url)
        os.remove(xiaomi_tmp)
        file_path = xiaomi_path+'/xiaomi.csv'
    except:
        file_path = '可能网络存在问题,请确定网络稳定的情况下再试.'
    return file_path


if __name__ == '__main__':
    run()