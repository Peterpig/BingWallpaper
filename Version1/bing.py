# -*- coding: utf-8 -*-

"""
每日下载bing搜索图片，并设置为壁纸
"""
import os
import json
import time
import urllib, urllib2
import win32gui,win32con,win32api

STORE_DIR = 'E:/BingPic/'

class BingPic(object):
    def __init__(self):
        self.api = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN'
        # 不存在创建目录
        if not os.path.exists(STORE_DIR):
            os.mkdir(STORE_DIR)

    def GetBingImageUrl(self):
        """调用接口，获取图片地址"""
        response = urllib2.urlopen(self.api)
        data = json.load(response)
        img_rul = data['images'][0]['url']
        return img_rul

    def DownLoadImg(self, url):
        if url.startswith('http'):
            pic_name = url[url.rfind('/')+1:]
            type = pic_name.split('.')[1]
            pic_name = STORE_DIR + time.strftime('%Y-%m-%d', time.localtime()) + '.%s' % type
            print u'准备下载：'+url
            urllib.urlretrieve(url, pic_name)
            print u'保存 %s 在当前路径下！' % pic_name
            return pic_name
        else:
            print ulr + '不是一个正确的图片地址'
            return -1

    def SetWallpaper(self, image_path):
        """设置背景"""
        k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\\\Desktop",0,win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2") #2拉伸适应桌面,0桌面居中
        win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,image_path, 1+2)
        print u'设置为桌面壁纸成功！'

if __name__ == '__main__':
    bing = BingPic()
    pic_ulr = bing.GetBingImageUrl()
    if pic_ulr != -1:
        pic_file = bing.DownLoadImg(pic_ulr)
        bing.SetWallpaper(pic_file)