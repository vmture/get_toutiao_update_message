#!/usr/bin/env
# -*- coding: utf-8 -*-
__author__ = 'Vmture'

import urllib
import os

def download_apk(folder_path, apk_name, download_url):
    """

    :param folder_path: 包下载的路径
    :param apk_name: 包的名字
    :param download_url: 下载url
    :return:
    """
    if apk_name not in os.listdir(folder_path):
        urllib.urlretrieve(download_url, folder_path+r'/'+apk_name)
