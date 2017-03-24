#!/usr/bin/env
# -*- coding: utf-8 -*-
__author__ = 'Vmture'
import os

files = ['小米', '百度', '腾讯', '360', '官网', 'appstore']

def create_folders():
    Desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    article_path = Desktop_path+r'/article_news'
    if 'article_news' not in os.listdir(Desktop_path):
        os.makedirs(article_path)
    for file in files:
        if file not in os.listdir(Desktop_path+r'/article_news'):
            os.makedirs(article_path+'/'+file)
    return article_path

if __name__ == '__main__':
    create_folders()