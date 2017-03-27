#!/usr/bin/env
# -*- coding: utf-8 -*-
__author__ = 'Vmture'

apple_rules = {
    "软件大小": r'<li><span class="label">大小： </span>([\d\.]+ MB)</li><li><span class="label">Apple',
    "版本号": r'<span itemprop="softwareVersion">(.+)</span></li><li><span class="label">',
    "更新日期": r'Etc/GMT">(.+)</span></li><li><span class="label">版本:',
    "本次更新": r'>本次更新<br>-([\x80-\xff]+)；<br>近期更新',
    "近期更新": r'近期更新<br>-(.+)；</p>'
}

baidu_rules_a = {
    "软件大小": 'class="size',
    "版本号": 'class="version',
    "包名": 'data_package',
    "下载地址": 'data_url',
    "应用介绍": r'<br>'
}

baidu_rules_b = {
    "软件大小": r'[\d\.]+M',
    "版本号": r'[\d\.]+',
    "包名": r'"(.+)"',
    "下载地址": r'"(.+)"',
    "应用介绍": r'>(.+)<br>今日头条'
}

tengxun_rules_a = {
    "软件大小": 'det-size',
    "版本号": 'det-othinfo-data',
    "更新时间": 'J_ApkPublishTime',
    "包名": 'apkName',
    "下载地址": 'downUrl',
    "更新内容": 'det-app-data-info' ,
    "appid": 'appId',
    "定位_a": 'var appDetailData = {',
    "定位_b": '}'
}

tengxun_rules_b = {
    "软件大小": r'[\d\.]+M',
    "版本号": r'>([\d\.V]+)<',
    "更新时间": r'data-apkPublishTime="(\d+)"',
    "包名": r'"(.+)"',
    "下载地址": r'"(.+)"',
    "更新内容": r'[\x80-\xff]+',
    "appid": r'\d+'
}

xiaomi_rules = {
    '定位_a': r'<ul class=" cf">(.+)</ul><div class="weight-font float-div">',
    '定位_b': r'<h3 class="special-h3">(.+)<h3 class="special-h3 ">',
    '软件大小': r'>([\d\.]+ M)<',
    '版本号': r'>([\d\.]+)<',
    '更新时间': r'>([\d\-]+)<',
    '包名': r'>([a-z\.]+)<',
    'appid': r'>(\d+)<',
    '下载地址': r'a href="([\/\w\?\=]+)" class="download"',
    '新版特性': '[\x80-\xff]+'
}

qihu_rules_a = {
    '软件大小': 'class="s-3"',
    '版本号': '版本：',
    '更新时间': '更新时间：',
    '包名': 'pname',
    '下载地址': 'downloadUrl',
    '定位_a': '更新内容',
    '定位_b': 'brief-toggle'
}

qihu_rules_b = {
    '软件大小': r'[\d\.]+M',
    '版本号': r'>([\d\.V]+)<',
    '更新时间': r'>([\d\-]+)<',
    '包名': r'"(.+)"',
    '下载地址': r"http.+apk",
    '更新内容': r'[\x80-\xff]+'
}

message_kinds_apple = ['查询时间', '软件大小', '版本号', '更新时间', '本次更新', '近期更新']
message_kinds_baidu = ['查询时间', '软件大小', '版本号', '包名', '应用介绍']
message_kinds_tengxun = ['查询时间', '软件大小', '版本号', '更新时间', '包名', 'appid', '更新内容']
message_kinds_xiaomi = ['查询时间', '软件大小', '版本号', '更新时间', '包名', 'appid', '新版特性']
message_kinds_360 = ['查询时间', '软件大小', '版本号', '更新时间', '包名', '更新内容']