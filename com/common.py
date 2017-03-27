#!/usr/bin/env
# -*- coding: utf-8 -*-
__author__ = 'Vmture'

import requests
from selenium import webdriver
import os
import codecs
import csv
import re
import urllib

class CommonFunction(object):
    def __init__(self):
        self.pj_path = os.path.join(os.path.expanduser("./tool"), 'phantomjs')
        self.desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
        self.desktop_contents = os.listdir(self.desktop_path)
        self.folders = ['小米', '百度', '腾讯', '360', '官网', 'apple']
        self.tags = ['查询时间', '软件大小', '版本号', '更新时间', '本次更新', '近期更新']
        self.folder_name = 'article_news'
        self.url_json_path = os.path.join(os.path.expanduser("./json"), 'urls.json')
        self.header_json_path = os.path.join(os.path.expanduser("./json"), 'headers.json')

    def create_folders(self):
        """
        生成今日头条文件夹
        """
        article_path = self.desktop_path+'/'+self.folder_name
        if self.folder_name not in self.desktop_contents:
            os.makedirs(article_path)
        for folder in self.folders:
            if folder not in os.listdir(article_path):
                os.makedirs(article_path+'/'+folder)

    def get_page_source_requests(self, url, name, headers=None):
        """
        use requests models to get page source,
        the page source will be saved to the tmp_path.
        :param url: 访问地址(str)
        :param name: tmp名字
        :param headers: 访问头,可为空(dist)
        """
        tmp_path = self._tmp_path(name)
        page_request = requests.get(url, headers=headers, timeout=10.0)
        page_source = page_request.content
        page_request.close()
        with open(tmp_path, 'wb') as F:
            F.write(page_source)

    def get_page_source_webdriver(self, url, name):
        """
        use selenuim.webdervier models to get page source,
        the page source will be saved to the tmp_path.
        :param url: 访问地址(str)
        :param name: tmp名字
        """
        tmp_path = self._tmp_path(name)
        driver = webdriver.PhantomJS(executable_path=self.pj_path)
        driver.get(url.encode('utf8'))
        page_source = driver.page_source
        driver.close()
        with open(tmp_path, 'wb') as F:
            F.write(page_source.encode('utf8'))

    def get_tmp_contents(self, name):
        """
        get the tmp contents about the page source
        :return: contents (list)
        """
        tmp_path = self._tmp_path(name)
        with open(tmp_path, 'r') as F:
            contents = F.readlines()
        return contents

    def _create_csv(self, csv_path, csv_name, comment_tags=None):
        """
        Create the csv which update messages about article news.
        :param comment_tags:csv文件的目录内容可为空,当为空时,取默认值(list)
                默认为['查询时间', '软件大小', '版本号', '更新时间', '本次更新', '近期更新']
        :param csv_path:csv文件存放的地址(str)
        :param csv_name:csv文件的命名(str)
        """
        file_path = csv_path+'/'+csv_name+'.csv'
        path = os.listdir(csv_path)
        if comment_tags is None:
            comment_tags = self.tags
        if csv_name+'.csv' not in path:
            with open(file_path, 'wb') as F:
                F.write(codecs.BOM_UTF8)
                csv_writer = csv.writer(F, dialect='excel')
                csv_writer.writerow(comment_tags)

    @classmethod
    def re_find_messages(cls, re_rule, re_contents):
        """
        通过re正则方式获取相应的内容
        :param re_rule: 正则的规则(str)
        :param re_contents: 需要正则查找的内容(str)
        :return:contents 通过正则查找到的序号为0的list内容(str)
        """
        if re.compile(re_rule).search(re_contents):
            contents = re.compile(re_rule).findall(re_contents)[0]
        else:
            print('re_rule or re_contents is wrong')
            print(re_rule)
            print(re_contents)
            contents = ''
        return contents

    def _insert_data(self, csv_path, csv_name, last_messages):
        """
        根据版本号判断(旧数据最后的版本号与查询时的版本号),是否插入新的数据到csv文件.
        :param csv_path:csv文件存放的地址(str)
        :param csv_name:csv文件的命名(str)
        :param last_messages: 最新查询到的内容(list)
        :return 更新了返回1,没有更新返回2
        """
        file_path = csv_path+'/'+csv_name+'.csv'
        old_data = list(csv.reader(open(file_path, 'r')))
        #根据版本号判断(旧数据最后的版本号与查询时的版本号)
        old_version_num = old_data[0].index('版本号')
        old_version = old_data[-1][old_version_num]
        last_version = last_messages[old_version_num]
        if last_version != old_version:
            with open(file_path, 'wb') as F:
                F.write(codecs.BOM_UTF8)
                csv_writer = csv.writer(F, dialect='excel')
                for contents in old_data:
                    csv_writer.writerow(contents)
                csv_writer.writerow(last_messages)
            return 1
        else:
            return 2

    def _get_apk_name(self, last_messages, folder_path, csv_name):
        """
        获取下载的apkname
        :param last_messages:最新信息
        :return:返回apkname
        """
        file_path = folder_path+'/'+csv_name+'.csv'
        old_data = list(csv.reader(open(file_path, 'r')))
        name_num = old_data[0].index('包名')
        version_num = old_data[0].index('版本号')
        apk_name = last_messages[name_num] + '_' + last_messages[version_num]+'.apk'
        return apk_name

    def _download_apk(self, last_messages, folder_path, download_url, csv_name):
        """
        下载最新的头条apk
        :param last_messages:最新信息
        :param folder_path: 包下载的路径
        :param download_url: 下载url
        :return:
        """
        apk_name = self._get_apk_name(last_messages, folder_path, csv_name)
        if apk_name not in os.listdir(folder_path):
            urllib.urlretrieve(download_url, folder_path+r'/'+apk_name)

    def find_url(self, name):
        """
        从urls.json文件中获取对应渠道名的url
        :param name:渠道名('str')
        :return:返回获取到的url
        """
        with open(self.url_json_path, 'r') as urls:
            url = eval(urls.read())[name]
        return url

    def find_header(self, name):
        """
        从headers.json文件中获取对应渠道名的headers
        :param name: 渠道名('str')
        :return:返回获取到的header
        """
        with open(self.header_json_path, 'r') as headers:
            header = eval(headers.read())[name]
        return header

    def _tmp_path(self, name):
        """
        返回tmp路径
        :param name:tmp名字(str)
        :return:返回tmp路径(str)
        """
        return '/tmp/tmp_'+name+'.txt'

    def run_a(self, csv_name, last_messages, comment_tags=None):
        """
        运行方法,无下载apk形式,返回csv路径和是否更新(0为异常,1为更新,2为没更新)
        :param csv_name:csv文件的命名(str)
        :param last_messages:最新查询到的内容(list)
        :param comment_tags:csv文件的目录内容可为空,当为空时,取默认值(list)
                默认为['查询时间', '软件大小', '版本号', '更新时间', '本次更新', '近期更新']
        :return:正常返回csv路径和是否更新(str)
        """
        article_path = self.desktop_path+'/'+self.folder_name
        folder_path = article_path+'/'+csv_name
        filename = folder_path+'/'+csv_name+'.csv'
        tmp_path = self._tmp_path(csv_name)
        try:
            self._create_csv(folder_path, csv_name, comment_tags)
            update_num = self._insert_data(folder_path, csv_name, last_messages)
            os.remove(tmp_path)
            return filename, update_num
        except:
            error_message = '可能网络存在问题,请确定网络稳定的情况下再试.'
            return error_message, 0

    def run_b(self, csv_name, last_messages, download_url, comment_tags=None):
        """
        运行方法,下载apk形式,返回csv路径和是否更新(0为异常,1为更新,2为没更新)
        :param csv_name:csv文件的命名(str)
        :param last_messages:最新查询到的内容(list)
        :param apk_name: 包的名字
        :param download_url: 下载url
        :param comment_tags:csv文件的目录内容可为空,当为空时,取默认值(list)
                默认为['查询时间', '软件大小', '版本号', '更新时间', '本次更新', '近期更新']
        :return:正常返回csv路径和是否更新(str)
        """
        article_path = self.desktop_path+'/'+self.folder_name
        folder_path = article_path+'/'+csv_name
        filename = folder_path+'/'+csv_name+'.csv'
        tmp_path = self._tmp_path(csv_name)
        try:
            self._create_csv(folder_path, csv_name, comment_tags)
            update_num = self._insert_data(folder_path, csv_name, last_messages)
            self._download_apk(last_messages, folder_path, download_url, csv_name)
            os.remove(tmp_path)
            return filename, update_num
        except:
            error_message = '可能网络存在问题,请确定网络稳定的情况下再试.'
            return error_message, 0
