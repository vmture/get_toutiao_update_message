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
                size=(200, 150))
        self.panel = wx.Panel(self, -1)
        button_x_pos = 200
        button_y_pos = 150
        self.button_run = wx.Button(self.panel, -1, u"run", pos=(button_x_pos/2-44, button_y_pos/4))

        self.Bind(wx.EVT_BUTTON, self.OnClick_run, self.button_run)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClick_run(self, event):
        self.thread_run()
        str = '查询完毕'
        dlg = wx.MessageDialog(None, str.decode(encoding='utf-8'), u'查询结果', wx.YES_DEFAULT)
        if dlg.ShowModal() == wx.ID_YES:
            dlg.Destroy()

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


if __name__ == '__main__':
    app = wx.App()
    frame = ButtonFrame()
    frame.Show()
    app.MainLoop()

