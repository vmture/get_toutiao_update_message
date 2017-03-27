#!/usr/bin/env
# -*- coding: utf-8 -*-
__author__ = 'vmture'

import csv

import wx

from new_script import qihu_new, apple_new, baidu_new, tengxun_new, xiaomi_new
from com.common import CommonFunction


class ButtonFrame(wx.Frame):
    def __init__(self):
        self.update = '渠道已更新\n\n'
        self.un_update = '渠道未更新\n\n'
        a = CommonFunction()
        a.create_folders()
        wx.Frame.__init__(self, None, -1, u'今日头条更新信息',
                size=(500, 150))
        self.panel = wx.Panel(self, -1)
        button_x_pos = 500
        button_y_pos = 300

        self.button_xiaomi = wx.Button(self.panel, -1, u"小米渠道", pos=(50, 20))
        self.button_baidu = wx.Button(self.panel, -1, u'百度渠道', pos=(button_x_pos/3+50, 20))
        self.button_tengxun = wx.Button(self.panel, -1, u'腾讯渠道', pos=(button_x_pos/3*2+50, 20))
        self.button_360 = wx.Button(self.panel, -1, u'360渠道', pos=(50, button_y_pos/5+20))
        self.button_apple = wx.Button(self.panel, -1, u'苹果渠道', pos=(button_x_pos/3+50, button_y_pos/5+20))
        self.button_guanwang = wx.Button(self.panel, -1, u'官网渠道', pos=(button_x_pos/3*2+50, button_y_pos/5+20))

        self.Bind(wx.EVT_BUTTON, self.OnClick_xiaomi, self.button_xiaomi)
        self.Bind(wx.EVT_BUTTON, self.OnClick_baidu, self.button_baidu)
        self.Bind(wx.EVT_BUTTON, self.OnClick_tengxun, self.button_tengxun)
        self.Bind(wx.EVT_BUTTON, self.OnClick_360, self.button_360)
        self.Bind(wx.EVT_BUTTON, self.OnClick_apple, self.button_apple)
        self.Bind(wx.EVT_BUTTON, self.OnClick_guanwang, self.button_guanwang)
        self.Bind(wx.EVT_CLOSE, self.OnClose)


    def OnClick_xiaomi(self, event):
        file_path, update = xiaomi_new.run()
        if update == 1:
            str = self.update
        else:
            str = self.un_update
        if 'csv' in file_path:
            datas = list(csv.reader(open(file_path, 'r')))
            str += '文件已创建,路径为:'+file_path+'\n'
            old_datas = datas[0]
            new_datas = datas[-1]
            for i in old_datas:
                str += i+':\n'
                str += new_datas[old_datas.index(i)]+'\n'
        else:
            str = file_path
        # self.text.SetValue(str)
        dlg = wx.MessageDialog(None, str.decode(encoding='utf-8'), u'小米渠道', wx.YES_DEFAULT)
        if dlg.ShowModal() == wx.ID_YES:
            dlg.Destroy()

    def OnClick_baidu(self, event):
        file_path, update = baidu_new.run()
        if update == 1:
            str = self.update
        else:
            str = self.un_update
        if 'csv' in file_path:
            datas = list(csv.reader(open(file_path, 'r')))
            str += '文件已创建,路径为:'+file_path+'\n'
            old_datas = datas[0]
            new_datas = datas[-1]
            for i in old_datas:
                str += i+':\n'
                str += new_datas[old_datas.index(i)]+'\n'
        else:
            str = file_path
        dlg = wx.MessageDialog(None, str.decode(encoding='utf-8'), u'百度渠道', wx.YES_DEFAULT)
        if dlg.ShowModal() == wx.ID_YES:
            dlg.Destroy()

    def OnClick_tengxun(self, event):
        file_path, update = tengxun_new.run()
        if update == 1:
            str = self.update
        else:
            str = self.un_update
        if 'csv' in file_path:
            datas = list(csv.reader(open(file_path, 'r')))
            str += '文件已创建,路径为:'+file_path+'\n'
            old_datas = datas[0]
            new_datas = datas[-1]
            for i in old_datas:
                str += i+':\n'
                str += new_datas[old_datas.index(i)]+'\n'
        else:
            str = file_path
        dlg = wx.MessageDialog(None, str.decode(encoding='utf-8'), u'腾讯渠道', wx.YES_DEFAULT)
        if dlg.ShowModal() == wx.ID_YES:
            dlg.Destroy()

    def OnClick_360(self, event):
        file_path, update = qihu_new.run()
        if update == 1:
            str = self.update
        else:
            str = self.un_update
        if 'csv' in file_path:
            datas = list(csv.reader(open(file_path, 'r')))
            str += '文件已创建,路径为:'+file_path+'\n'
            old_datas = datas[0]
            new_datas = datas[-1]
            for i in old_datas:
                str += i+':\n'
                str += new_datas[old_datas.index(i)]+'\n'
        else:
            str = file_path
        dlg = wx.MessageDialog(None, str.decode(encoding='utf-8'), u'360渠道', wx.YES_DEFAULT)
        if dlg.ShowModal() == wx.ID_YES:
            dlg.Destroy()

    def OnClick_apple(self, event):
        file_path, update = apple_new.run()
        if update == 1:
            str = self.update
        else:
            str = self.un_update
        if 'csv' in file_path:
            datas = list(csv.reader(open(file_path, 'r')))
            str += '文件已创建,路径为:'+file_path+'\n'
            old_datas = datas[0]
            new_datas = datas[-1]
            for i in old_datas:
                str += i+':\n'
                str += new_datas[old_datas.index(i)]+'\n'
        else:
            str = file_path
        dlg = wx.MessageDialog(None, str.decode(encoding='utf-8'), u'苹果渠道', wx.YES_DEFAULT)
        if dlg.ShowModal() == wx.ID_YES:
            dlg.Destroy()

    def OnClick_guanwang(self, event):
        dlg = wx.MessageDialog(None, u'功能还未完成', u'官网渠道', wx.YES_DEFAULT)
        if dlg.ShowModal() == wx.ID_YES:
            dlg.Destroy()

    def OnClose(self, event):
        wx.Exit()
        self.panel.Destroy()



if __name__ == '__main__':
    app = wx.App()
    frame = ButtonFrame()
    frame.Show()
    app.MainLoop()

