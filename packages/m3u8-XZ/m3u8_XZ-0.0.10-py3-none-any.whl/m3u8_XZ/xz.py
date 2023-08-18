# -- coding:utf-8 --
# Time:2023-03-23 10:48
# Author:XZ
# File:xz.py
# IED:PyCharm
import time
from threading import Thread

import aiohttp
import asyncio
import requests as req
import re
import os
from .cryptoModel import DecodeByte


class M3U8:
    """
        url: m3u8文件的url
        folder: 下载文件后存储的名字
        run(): 执行下载
    """
    print_callback = None
    logger = None

    def __init__(self, url=None, folder='m3u8_XZ_test', path='./down_load/', m3u8_file=None, logger=True, headers=None, print_callback=None):
        # 下载文件名
        self.file_name = folder + '.mp4'
        # 下载存储文件夹
        self.path = os.path.join(path, folder)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        # 缓存文件夹
        self.temp_path = os.path.join(self.path, 'temp')
        if not os.path.exists(self.temp_path):
            os.makedirs(self.temp_path)
        # m3u8
        self.url = url
        if headers:
            self.headers = headers
        else:
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
            }
        self.m3u8_file = m3u8_file
        # 记录进度
        self.list_length = 0
        self.num = 0
        # 有序存储ts列表文件
        self.ts_list = list()
        # 解密处理
        self.cry = {
            "key": "",
            "iv": "",
            "method": "",
        }
        #
        M3U8.print_callback = print_callback
        M3U8.logger = logger

    # 通过ts名称，转换ts网址
    @staticmethod
    def get_full_ts_url(url, ts_name: str):
        # 直接返回http地址
        if ts_name.startswith("http"):
            return ts_name
        # 需要拼接完整url地址
        # 分割ts name
        tl = ts_name.split('/')
        #
        new_url = []
        # 循环url，去掉ts name中重复的部分
        for s in url.split('/')[:-1]:
            if s in tl:
                tl.remove(s)
            new_url.append(s)
        # 拼接ts name
        new_url.extend(tl)
        result = '/'.join(new_url)
        # 返回
        return result

    # 通过url，获取ts列表
    def get_ts_list(self) -> list:
        # 通过本地文件获取
        if self.m3u8_file:
            with open(self.m3u8_file, 'r', encoding='utf8') as f:
                text = f.read()
        # 通过url获取m3u8文件内容
        elif self.url:
            res = req.get(self.url, headers=self.headers, verify=False)
            if res.status_code != 200:
                raise Exception('请求失败,m3u8地址不存在')
            text = res.text
        # 设置加密参数
        self.set_cry(text, self.url)
        # 去掉注释
        ts_str = re.sub('#.*?\n', '', text)
        # 转为列表
        self.ts_list = ts_str.split('\n')
        self.list_length = len(self.ts_list)

        return self.ts_list

    def set_cry(self, text, url=""):
        # 获取加密参数
        x_key = re.findall('#EXT-X-KEY:(.*?)\n', text)
        cry_obj = dict()
        if len(x_key) > 0:
            # 提取
            for item in x_key[0].split(','):
                key = item.split('=')[0]
                value = item.replace(key, '')[1:].replace('"', '')
                cry_obj[key] = value
            # format
            if cry_obj.get('URI') and not cry_obj['URI'].startswith('http'):
                cry_obj['URI'] = self.get_full_ts_url(url, cry_obj['URI'])
                # 获取key
                res = req.get(cry_obj['URI'], headers=self.headers)
                self.cry['key'] = res.content
            # 加密方式
            self.cry['method'] = cry_obj.get('METHOD')
            # iv值
            if cry_obj.get('IV'):
                self.cry['iv'] = cry_obj['IV'][2:18]

        else:
            pass

    # 通过ts列表，异步缓存所有ts文件
    async def get_data(self):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            tasks = []
            for index, ts in enumerate(self.get_ts_list(), 1):
                if ts:
                    # 给ts重命名，为了排序
                    temp_ts = str(index).zfill(6) + '.mp4'
                    # 创建task任务
                    task = asyncio.create_task(self.down_file(session, self.get_full_ts_url(self.url, ts), temp_ts))
                    tasks.append(task)
            # 添加到事件循环
            await asyncio.wait(tasks)

    # 异步下载二进制文件
    async def down_file(self, session, url, ts_name):
        async with session.get(url, ssl=False) as res:
            try:
                data = await res.read()
            except Exception as e:
                M3U8.log(e)
                return False
            # 如果有加密，需要data解密后再存储
            if self.cry.get('key'):
                # 如果源文件有iv就读取，如果没有就用文件名
                iv = self.cry["iv"] if self.cry.get("iv") else ts_name.split('.')[0].zfill(16)
                data = DecodeByte.do_decode(self.cry["key"], iv, data, self.cry["method"])
                if not data:
                    raise Exception('解密失败')
            # 保存
            with open(os.path.join(self.temp_path, ts_name), 'wb') as f:
                f.write(data)
                # 打印进度
                self.num += 1
                M3U8.log('\r下载中:{:3.0f}%| {}/{}'.format(self.num / self.list_length * 100, self.num, self.list_length),
                          end='', flush=True)
                #
                if M3U8.print_callback:
                    M3U8.print_callback(loaded_num=self.num, load_count=self.list_length)

    # 通过名称按序读取ts文件，整合成一个ts文件
    @staticmethod
    def combine_ts(source_path, dest_file):
        # 获取所有缓存文件
        file_list = os.listdir(source_path)
        if not file_list:
            return
        # 名称排序
        file_list.sort(key=lambda s: s.split('.')[0])
        # 文件总数
        length = len(file_list)
        # 开始合并文件
        with open(dest_file, 'ab') as f:
            # 循环文件列表
            for i, file in enumerate(file_list):
                # 读取每个文件
                with open(os.path.join(source_path, file), 'rb') as rf:
                    # 把每个文件的内容 追加到同一个文件
                    data = rf.read()
                    f.write(data)
                # 清除缓存文件
                os.remove(os.path.join(source_path, file))
                # 打印进度
                M3U8.log('\r合并中:{:3.0f}%'.format(i / length * 100), end='', flush=True)
                #
                if M3U8.print_callback:
                    M3U8.print_callback(combined_num=i, combine_count=length)
        # 移除缓存文件夹
        os.rmdir(source_path)

    # 异步启动器
    def run(self, loop=None):
        if self.url or self.m3u8_file:
            stime = time.time()
            if not loop:
                loop = asyncio.get_event_loop()
            loop.run_until_complete(self.get_data())
            M3U8.log('下载完成，准备合并...')
            time.sleep(2)
            self.combine_ts(self.temp_path, os.path.join(self.path, self.file_name))
            over_time = time.time() - stime
            M3U8.log('\nover time : ', over_time)
            if M3U8.print_callback:
                M3U8.print_callback(over_time=over_time)

    @staticmethod
    def log(*args, **kwargs):
        if M3U8.logger:
            print(*args, **kwargs)

    def run_thread(self):
        if self.url or self.m3u8_file:
            # 创建事件循环对象
            loop = asyncio.new_event_loop()
            # 创建子线程并启动异步任务
            thread = Thread(target=self.run, args=(loop,), daemon=True)
            thread.start()

