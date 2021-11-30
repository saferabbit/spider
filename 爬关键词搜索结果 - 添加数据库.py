# -*- coding:utf-8 -*-
"""
作者：safe_rabbit
日期：2021年07月29日
"""
import random
from 数据库 import db, Sif_search, Amazon123_rank
import json
import requests
import time
from loguru import logger
import csv
import easygui as g

logger.add('runtime.log', format="{time} {level} {message}", level="INFO")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                  '94.0.4606.71 Safari/537.36',
    'Referer': 'https://www.sif.com/compete?country=US',
    'Host': 'www.sif.com',
    'Origin': 'https://www.sif.com',
    'authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3ZWNoYXRpZCI6Im90SkwwNXdrZDB5X2xEZkl1MTJYa09f'
                     'ZV9HV3ciLCJleHAiOjE2MzQwMjMyMTEsInVzZXJpZCI6ImszcEI4Nng5RjE4MTNuVmw5Mmc5VjQ0WiJ9.eBDM'
                     'xBF_DdKffanq4m9OSJsJwYr7BiJkbXCypQbZoMQ'
}


# payload = {'keyword': "cake"}
# t = time.time()  # 获取时间戳
# urlt = str(round(t * 1000))
# url = 'https://www.sif.com/api/search/keywordOverview?_t=' + urlt
# r = requests.post(url, json=payload, headers=headers)
# data=json.dumps(payload)
# print(r.json())

@logger.catch()
def get_html(url, payload, headers):
    html = requests.post(url, json=payload, headers=headers)  # 发出POST请求

    if html.status_code == 200:  # 状态码

        parse_html(html=html.json())  # 获取Json数据
        # print(html.json())
    else:
        print('访问网页错误')


def parse_html(html):
    name_1 = list()  # 搜索词
    name_2 = list()  # 月搜索量
    name_3 = list()  # 竞品数
    name_4 = list()  # 自然搜索产品
    name_5 = list()  # PPC广告产品
    data = html['data']  # 获取JSON里的目标数据
    print(data)
    # for i in range(len(data)):
    try:
        # Monthly_search_volume = data['estSearchesNum']
        print(data['estSearchesNum'])
        # Natural_Search_Products = data['nfAsinNum']
        # Number_of_competing_products = data['saleNum']
        # PPC_advertising_products = data['ppcAdAsinNum']
        # search_name = data['keyword']
        # name_1.append(search_name)
        # name_2.append(Monthly_search_volume)
        # name_3.append(Number_of_competing_products)
        # name_4.append(Natural_Search_Products)
        # name_5.append(PPC_advertising_products)
        # for item in range(len(name_1)):
        data_1 = Sif_search(search_name=data['keyword'],
                          Monthly_search_volume=data['estSearchesNum'],
                          Number_of_competing_products=data['saleNum'],
                          Natural_Search_Products=data['nfAsinNum'],
                          PPC_advertising_products=data['ppcAdAsinNum'])
        db.session.add(data_1)
        db.session.commit()
    except:
        pass
    # print(name_1, name_2, name_3, name_4, name_5)


@logger.catch()
def write_excel(data, head):
    # datas = pd.DataFrame(data, columns=head)
    # datas.to_csv('D:/test.csv', index=False, encoding='gbk')
    # test.csv表示如果在当前目录下没有此文件的话，则创建一个csv文件
    # a表示以“追加”的形式写入，如果是“w”的话，表示在写入之前会清空原文件中的数据
    # newline是数据之间不加空行
    # encoding='utf-8'表示编码格式为utf-8，如果不希望在excel中打开csv文件出现中文乱码的话，将其去掉不写也行。
    with open('D:/test.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=head)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
        # writer.writeheader()  # 写入列名
        writer.writerows(data)  # 写入数据


def pd_list():
    search_term = Amazon123_rank.query(Amazon123_rank.Search_term).all
    print(search_term)
    return search_term


if __name__ == '__main__':
    db.create_all()  # 创建表
    # datas = list()  # 汇总
    heads = ['搜索词', '月搜索量', '竞品数', '自然搜索产品', 'PPC广告产品']  # 设置标头内容
    # search_term1 = Amazon123_rank.query.get(1)
    # print(search_term1.Search_term)
    first_col = Amazon123_rank.query.all()
    for i in range(len(first_col)):
        try:
            if 1 <= i < 10:
                # print('这是第{}个'.format(i))
                key = first_col[i].Search_term  # A列单个赋值
                payload = {'keyword': key}  # 输入POST信息
                print(payload)
                t = time.time()  # 获取时间戳
                urlt = str(round(t * 1000))
                url = 'https://www.sif.com/api/search/keywordOverview?country=US&_t=' + urlt
                get_html(url, payload=payload, headers=headers)
                # print(datas)
                tc = random.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
                time.sleep(tc)
            else:
                continue
        except:
            break
    print('爬取完毕')
    # write_excel(data=datas, head=heads)
    g.msgbox(title='运行结束', msg='爬取完成')
