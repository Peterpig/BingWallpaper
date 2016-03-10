# -*- coding: utf-8 -*-

import base64
import json
from Tkinter import *
import os
from PIL import Image, ImageTk
import tkFileDialog
import tkMessageBox
import win32gui,win32con,win32api
import urllib2
import zlib


class BingPicTk(object):
    def __init__(self):
        self.STORE_DIR = 'E:/BingPic/'
        self.top = Tk()
        self.api = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=500&mkt=zh-CN'
        self.top.title('BingWallpaper V2.0')
        # bmp = BitmapImage(file="bing.ico") 
        self.top.geometry('680x500')
        self.img_id = 0
        self.img_path  = ''
        if not os.path.exists(self.STORE_DIR):
            os.mkdir(self.STORE_DIR)

        # 文件选择框
        self.top_frame = Frame(self.top)
        self.img_path = Label(self.top_frame, text='图片保存目录：', font=('', 14)).grid(row=0, column=0)
        self.str = StringVar()
        self.str.set(self.STORE_DIR)
        self.dir_choose = Entry(self.top_frame, textvariable=self.str, state='readonly')
        self.dir_choose.grid(row=0, column=1, columnspan=5, pady=20)

        # 选择按钮
        self.dir_choose_btn = Button(self.top_frame, text='选择', command=self.ok, padx=10, activebackground='#ccc')
        self.dir_choose_btn.grid(row=0, column=6, padx=20)

        # 更新按钮
        self.update_btn = Button(self.top_frame, text='下一张', command=self.update_img, padx=20, activebackground='#ccc')
        self.update_btn.grid(row=0, column=7, padx=10)

        # 设置按钮
        self.set_btn = Button(self.top_frame, text='设置壁纸', command=self.set_wallpape, padx=20, activebackground='#ccc')
        self.set_btn.grid(row=0, column=8, padx=10)

        self.top_frame.pack()

        # 显示图片
        self.img_frame = Frame(self.top)
        img = '' # self.init_pic(self.STORE_DIR+'1.bmp')
        self.label_img = Label(self.img_frame, image=img)
        self.label_img.pack(side='top')
        self.img_frame.pack()

    def ok(self):
        path = tkFileDialog.askdirectory(title='请选择图片保存位置', initialdir=self.STORE_DIR)
        if path:
            path += '/'
            self.str.set(path)
            self.STORE_DIR = path

    def down_load_img(self, url):
        import time
        import urllib
        if url.startswith('http'):
            pic_name = url[url.rfind('/')+1:]
            name, type = pic_name.split('.')
            pic_name = self.STORE_DIR + time.strftime('%Y-%m-%d', time.localtime()) + '%s.%s' % (name, type)
            urllib.urlretrieve(url, pic_name)

            bmpImage = Image.open(pic_name)
            newPath = pic_name.replace('jpg', 'bmp')
            bmpImage.save(newPath, 'BMP')
            os.remove(pic_name)
            return newPath
        else:
            print ulr + '不是一个正确的图片地址'
            return -1

    def get_bing_img_url(self):
        """调用接口，获取图片地址"""
        response = urllib2.urlopen(self.api)
        data = json.load(response)
        try:
            img_url = data['images'][self.img_id]['url']
            self.img_id += 1
        except Exception, e:
            img_url = data['images'][0]['url']
            self.img_id = 0
            tkMessageBox.showinfo('警告', '没有图片啦！')
        return img_url

    def init_pic(self, pic_path):
        img = Image.open(pic_path)
        img = img.resize((680, 500), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        return img

    def update_img(self):
        url = self.get_bing_img_url()
        pic_path = self.down_load_img(url)
        img = self.init_pic(pic_path)
        self.label_img.configure(image=img)
        self.label_img.image = img
        self.image_path = pic_path

    def set_wallpape(self):
        """设置背景"""
        k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2") #2拉伸适应桌面,0桌面居中
        win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, self.image_path, 1+2)
        print u'设置为桌面壁纸成功！'

def main():
    bing = BingPicTk()
    mainloop()

if __name__ == '__main__':
    main()