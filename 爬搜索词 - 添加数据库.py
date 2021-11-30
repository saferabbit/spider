# -*- coding:utf-8 -*-
"""
作者：safe_rabbit
日期：2021年07月27日
"""
import requests
from bs4 import BeautifulSoup
from 数据库 import db, Amazon123_rank, Amazon123_increase
from loguru import logger

logger.add('runtime.log', format="{time} {level} {message}", level="INFO")


@logger.catch()
def getdata_rank(url):
    strhtml = requests.get(url, headers=headers)
    soup = BeautifulSoup(strhtml.text, 'lxml')
    data1 = soup.select('div.listdata>div:nth-child(1)')
    term = list()
    for i in data1:
        term.append(i.get_text())

    data2 = soup.select('div.listdata>div:nth-child(2)')
    rank = list()
    for i in data2:
        rank.append(i.get_text())

    data3 = soup.select('div.listdata>div:nth-child(3)')
    last_rank = list()
    for i in data3:
        last_rank.append(i.get_text())

    data4 = soup.select('div.listdata>div:nth-child(4)')
    rank_rise_fall = list()
    for i in data4:
        rank_rise_fall.append(i.get_text())

    data5 = soup.select('div.listdata>div:nth-child(1)>a')
    link = list()
    for i in data5:
        link.append(i.get('href'))

    for i in range(len(term)):
        # print('第{}个写入数据库'.format(i+1))
        data = Amazon123_rank(Search_term=term[i],
                         Ranking_this_week=rank[i],
                         Last_weeks_ranking=last_rank[i],
                         Ranking_rise_and_fall=(int(last_rank[i])-int(rank[i])),
                         link=link[i])
        db.session.add(data)
        db.session.commit()

    # for item in zip(term, rank, last_rank, rank_rise_fall, link):
    #     datas.append({
    #         'Search_term': item[0],
    #         'Ranking_this_week': item[1],
    #         "Last_weeks_ranking": item[2],
    #         'Ranking_rise_and_fall': (int(item[2])-int(item[1])),
    #         'link': item[4]
    #     })
    #     print(datas)


@logger.catch()
def getdata_increase(url):
    strhtml = requests.get(url, headers=headers)
    soup = BeautifulSoup(strhtml.text, 'lxml')
    data1 = soup.select('div.listdata>div:nth-child(1)')
    term = list()
    for i in data1:
        term.append(i.get_text())

    data2 = soup.select('div.listdata>div:nth-child(2)')
    rank = list()
    for i in data2:
        rank.append(i.get_text())

    data3 = soup.select('div.listdata>div:nth-child(3)')
    last_rank = list()
    for i in data3:
        last_rank.append(i.get_text())

    data4 = soup.select('div.listdata>div:nth-child(4)')
    rank_rise_fall = list()
    for i in data4:
        rank_rise_fall.append(i.get_text())

    data5 = soup.select('div.listdata>div:nth-child(1)>a')
    link = list()
    for i in data5:
        link.append(i.get('href'))

    for i in range(len(term)):
        # print('第{}个写入数据库'.format(i+1))
        data = Amazon123_increase(Search_term=term[i],
                         Ranking_this_week=rank[i],
                         Last_weeks_ranking=last_rank[i],
                         Ranking_rise_and_fall=(int(last_rank[i])-int(rank[i])),
                         link=link[i])
        db.session.add(data)
        db.session.commit()


# def makedata(datas_1, datas_2, heads):
#     datas = pd.DataFrame(datas_1, columns=heads)
#     datas2 = pd.DataFrame(datas_2, columns=heads)
#     with pd.ExcelWriter('D:/test.xlsx') as writer:
#         datas.to_excel(writer, index=0, sheet_name='排名')
#         datas2.to_excel(writer, index=0, sheet_name='涨幅')


if __name__ == '__main__':
    db.create_all()  # 创建表
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                      '/91.0.4472.164 Safari/537.36'}
    # head = ['搜索词', '本周排名', '上周排名', '排名涨跌', 'link']
    # datas_rank_1 = list()
    # datas_rank_2 = list()
    for i in range(1, 18):
        url = 'https://www.amz123.com/usatopkeywords-{}-1-.htm?rank=&uprank='.format(i)
        getdata_rank(url=url)
    print('完成排名的第一个')
    for i in range(1, 18):
        url = 'https://www.amz123.com/usatopkeywords-{}-1-.htm?rank=10001_50000&uprank=0'.format(i)
        getdata_rank(url=url)
    print('完成排名的第二个')
    for i in range(1, 18):
        url = 'https://www.amz123.com/usatopkeywords-{}-1-.htm?rank=50000&uprank=0'.format(i)
        getdata_rank(url=url)
    print('完成排名的第三个')
    for i in range(1, 18):
        url = 'https://www.amz123.com/usatopkeywords-{}-1-.htm?rank=0&uprank=1000'.format(i)
        getdata_rank(url=url)
    print('完成涨幅的第一个')
    for i in range(1, 18):
        url = 'https://www.amz123.com/usatopkeywords-{}-1-.htm?rank=10001_50000&uprank=1000'.format(i)
        getdata_rank(url=url)
    print('完成涨幅的第二个')
    for i in range(1, 18):
        url = 'https://www.amz123.com/usatopkeywords-{}-1-.htm?rank=50000&uprank=1000'.format(i)
        getdata_rank(url=url)
    print('完成涨幅的第三个')

    # makedata(datas_1=datas_rank_1, datas_2=datas_rank_2, heads=head)
