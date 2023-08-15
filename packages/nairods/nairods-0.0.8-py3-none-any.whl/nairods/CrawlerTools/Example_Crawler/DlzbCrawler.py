#! /usr/bin/env python
# -*-coding:utf-8-*-
import os
import requests
import pandas as pd
from lxml import etree
from pathlib import Path


# 完成电力招标网的信息抓取
class CrawlerCurd(object):
    """
    爬虫增删改查
    """

    def __init__(self, url):
        self.url = url
        self.headers = {"Content-Type": "application/json"}

    def req_get(self):
        """
        get请求
        :return:
        """
        result = requests.get(self.url, headers=self.headers)
        html = etree.HTML(result.text)
        area_data = []
        title_data = []
        url_data = []
        date_data = []
        for i in range(1, 13):
            area_xpath = html.xpath(f'//*[@id="con_two_1"]/ul/li[{i}]/span[2]/a')  # 区域
            title_xpath = html.xpath(f'//*[@id="con_two_1"]/ul/li[{i}]/a')  # 标题,url
            date_xpath = html.xpath(f'//*[@id="con_two_1"]/ul/li[{i}]/span[1]')  # 日期

            for area in area_xpath:
                area_data.append(area.text)

            for div in title_xpath:
                title_data.append(div.text)
                url_data.append(div.attrib.get("href"))

            for div in date_xpath:
                date_data.append(div.text)

        area = pd.Series(area_data, name='区域')
        title = pd.Series(title_data, name='标题')
        title_link = pd.Series(url_data, name='标题链接')
        collect_time = pd.Series(date_data, name='日期')
        df = pd.concat([area, title, title_link, collect_time], axis=1)

        # keywords_names = ["风电", "风机", "光伏"]
        # keywords_behavior = ["运行", "维护", "运维", "委托", "外委"]
        # 删除标题中的空格
        df['标题'] = df['标题'].str.replace(' ', '')
        # df.to_csv("excs.csv", index=False)
        # 使用正则表达式筛选同时包含 keywords_names 和 keywords_behavior 列表中至少一项关键词的标题
        # keywords_names = '|'.join(keywords_names)
        # keywords_behavior = '|'.join(keywords_behavior)
        # df = df[df['标题'].str.contains(keywords_names) & df['标题'].str.contains(keywords_behavior)]
        from datetime import datetime
        # 获取当前时间
        current_time = datetime.now()
        # 格式化日期和时间
        current_time = current_time.strftime("%Y-%m-%d-%H-%M-%S")
        from FilesTools import FileTools
        save_csv_folder = Path("../../Temp/Csv")
        if not os.path.exists(save_csv_folder):
            os.makedirs(save_csv_folder, exist_ok=True)
        save_csv_path = save_csv_folder / (F'电力招标网-{current_time}.csv')
        df.to_csv(save_csv_path, index=False)
        # print(df_filtered)
        return df

if __name__ == '__main__':
    # 完成电力招标网的信息抓取
    url = r"https://www.dlzb.com/zb/"
    CC = CrawlerCurd(url)
    CC.req_get()  # 保存结果为csv
