#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/9/4 0:50
@File  : downloadUtils.py
'''
''' 下载资源 '''

import os
import requests
import threading
from tkinter import *
from tkinter import filedialog

class Downloader:
    def __init__(self, url, num_threads, save_path):
        self.url = url
        self.num_threads = num_threads
        self.save_path = save_path
        self.filename = url.split('/')[-1]
        self.file_size = int(requests.head(self.url).headers['Content-Length'])

    def download(self, start, end, filename):
        if os.path.exists(filename):
            first_byte = os.path.getsize(filename)
        else:
            first_byte = start
        if first_byte >= end:
            return

        headers = {'Range': 'bytes=%d-%d' % (first_byte, end)}
        r = requests.get(self.url, headers=headers, stream=True)

        with open(filename, 'ab') as fp:
            fp.write(r.content)

    def multi_thread_download(self):
        part = self.file_size // self.num_threads
        for i in range(self.num_threads):
            start = part * i
            if i == self.num_threads - 1:
                end = self.file_size
            else:
                end = start + part
            t = threading.Thread(target=self.download, args=(start, end, self.save_path + '/part%d' % i))
            t.setDaemon(True)
            t.start()

        main_thread = threading.current_thread()
        for t in threading.enumerate():
            if t is main_thread:
                continue
            t.join()
        self.merge_files()

    def merge_files(self):
        with open(self.save_path + '/' + self.filename, 'wb') as fp:
            for i in range(self.num_threads):
                with open(self.save_path + '/part%d' % i, 'rb') as f:
                    fp.write(f.read())
                os.remove(self.save_path + '/part%d' % i)

def download_file():
    url = url_entry.get()
    save_path = path_entry.get()
    num_threads = int(thread_entry.get())
    downloader = Downloader(url, num_threads, save_path)
    downloader.multi_thread_download()

def browse_directory():
    directory = filedialog.askdirectory()
    path_entry.delete(0, END)
    path_entry.insert(0, directory)

root = Tk()
root.title('Downloader')

url_label = Label(root, text='URL:')
url_label.grid(row=0, column=0)
url_entry = Entry(root, width=50)
url_entry.grid(row=0, column=1)

path_label = Label(root, text='Save Path:')
path_label.grid(row=1, column=0)
path_entry = Entry(root, width=50)
path_entry.grid(row=1, column=1)
path_button = Button(root, text='Browse', command=browse_directory)
path_button.grid(row=1, column=2)

thread_label = Label(root, text='Number of Threads:')
thread_label.grid(row=2, column=0)
thread_entry = Entry(root, width=50)
thread_entry.grid(row=2, column=1)

download_button = Button(root, text='Download', command=download_file)
download_button.grid(row=3, column=1)

root.mainloop()

