# -*- coding:utf-8 -*-
"""
作者: gaoxu
日期: 2022年01月19日
"""
# 需求：获取梨视频网站上一个模块下的任意视频资源
import random
import json
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor


def task(this_dic):
    url = this_dic['url']
    name = this_dic['name']
    print('开始传输:', name)
    video_data = requests.get(url=url, headers=head).content
    print('传输结束', name)
    return name, video_data


def call_back(res_tuple):
    print('开始写入本地:', res_tuple.result()[0])
    with open(r'../gotpages/' + res_tuple.result()[0] + '.mp4', 'wb') as steam:
        steam.write(res_tuple.result()[1])
    print('本地完成:', res_tuple.result()[0])


def switch(dic_obj, video_id):
    fake_url = dic_obj['videoInfo']['videos']['srcUrl']
    index = fake_url.rfind('/')
    to_replace = fake_url[index + 1:index + 1 + 13]
    true_url = fake_url.replace(to_replace, 'cont-' + video_id)
    dic_obj['videoInfo']['videos']['srcUrl'] = true_url


if __name__ == '__main__':
    print('开始！')
    url = 'https://www.pearvideo.com/category_5'
    head = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36'
    }
    response = requests.get(url=url, headers=head)
    video_urls_names = []
    if response.status_code == 200:
        page_text = response.text
        tree = etree.HTML(page_text)
        lis = tree.xpath('//*[@id="listvideoListUl"]/li')

        for li in lis:
            detail_page_src = li.xpath('.//a/@href')[0]
            detail_page_url = 'https://www.pearvideo.com/' + detail_page_src
            video_id = detail_page_src.split('_')[1]
            video_name = li.xpath('.//div[@class="vervideo-title"]/text()')[0]
            # 视频地址是用ajax加载的
            ajax_url = 'https://www.pearvideo.com/videoStatus.jsp?'
            params = {
                'contId': video_id,
                'mrd': str(random.random())
            }
            head = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36',
                # 有这个才会拿到response
                'Referer': detail_page_url
            }
            response2 = requests.get(url=ajax_url, headers=head, params=params)
            # 返回json串
            dic_obj = response2.json()
            print(dic_obj)
            # 真假网址替换
            switch(dic_obj, video_id)
            print(dic_obj)
            # 将所有视频网址和名字取得并封装成字典
            dic_url_names = {
                'url': dic_obj['videoInfo']['videos']['srcUrl'],
                'name': video_name
            }
            # 将每一个视频信息对应的字典都整合到一起
            video_urls_names.append(dic_url_names)
    if len(video_urls_names) != 0:
        # 使用线程池对视频数据进行请求
        with ThreadPoolExecutor(max_workers=4) as pool:
            for i in range(0, len(video_urls_names)):
                res = pool.submit(task, video_urls_names[i])
                res.add_done_callback(call_back)
    print('结束！')
