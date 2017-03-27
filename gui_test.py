#!/usr/bin/env
# -*- coding: utf-8 -*-
__author__ = 'vmture'

import csv
import time
import wx

from new_script import qihu_new, apple_new, baidu_new, tengxun_new, xiaomi_new
import threading
from com.common import CommonFunction



class ButtonFrame(wx.Frame):
    def __init__(self):
        a = CommonFunction()
        a.create_folders()
        self.run_queue = [threading.Thread(target=apple_new.run), threading.Thread(target=qihu_new.run), threading.Thread(target=baidu_new.run), threading.Thread(target=tengxun_new.run), threading.Thread(target=xiaomi_new.run)]
        wx.Frame.__init__(self, None, -1, u'今日头条更新信息',
                size=(500, 150))
        self.panel = wx.Panel(self, -1)
        button_x_pos = 500
        button_y_pos = 300
        self.count = 0
        self.gauge = wx.Gauge(self.panel, -1, 100, (100, 50), (300, 30), style = wx.GA_PROGRESSBAR)
        self.gauge.SetBezelFace(3)
        self.gauge.SetShadowWidth(3)
        self.Center(True)

        self.Bind(wx.EVT_BUTTON, self.OnClick_run, self.button_run)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        # self.Bind(wx.EVT_IDLE, self.OnIdle)
        # self.button_xiaomi.SetDefault()
        # self.button_online.SetDefault()
        # self.button_cancel.SetDefault()
        # self.text = wx.TextCtrl(self.panel, pos=(30, 60), size=(430, 400), style = wx.TE_MULTILINE|wx.TE_RICH2)

    def OnClick_run(self, event):
        self.Bind(wx.EVT_IDLE, self.run)

    def run(self):
        time.sleep(5)
        thread = threading.Thread(target=self.test())
        thread.start()
        for i in xrange(10):
            threads_a = threading.enumerate()[1:]
            while True:
                threads_b = threading.enumerate()[1:]
                wx.Sleep(2)
                if threads_a != threads_b:
                    self.count += 1
                    self.dialog.Update(self.count)
                    break
        self.dialog.Destroy()
        # for thread in self.run_queue:
        #     print(thread)
        #     print(thread.name)
        #     print(threading.enumerate())
        #     while True:
        #         if threading.activeCount() < 3:
        #             thread.start()
        #             break
        # while True:
        #     print(threading.enumerate())
        #     time.sleep(5)
        #     if threading.activeCount() == 1:
        #         print('done')
        #         break



    def OnClose(self, event):
        wx.Exit()
        self.panel.Destroy()

    def thread_run(self):
        for thread in self.run_queue:
            thread.start()
            print(thread)
            print(thread.name)
            print(threading.enumerate())
            while True:
                if threading.activeCount() < 3:
                    break
        while True:
            print(threading.enumerate())
            time.sleep(5)
            if threading.activeCount() == 1:
                print('done')
                break

    def test(self):
        for i in xrange(10):
            thread = threading.Thread(target=self.sleep)
            thread.start()
            while True:
                time.sleep(5)
                if threading.activeCount() < 2:
                    break

    def sleep(self):
        time.sleep(5)


if __name__ == '__main__':
    app = wx.App()
    frame = ButtonFrame()
    frame.Show()
    app.MainLoop()

