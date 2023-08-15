#! /usr/bin/env python
# -*-coding:utf-8-*-
import pandas as pd
# ! /usr/bin/env python
# -*-coding:utf-8-*-

from bs4 import BeautifulSoup


# 临时文件操作的增删改查等
class TmpCurd(object):
    """
    临时文件操作
    不限于表格,文本等等
    """

    def __init__(self, tmp_file=""):
        self.tmp_file = tmp_file

    def read_temp(self, tmp_file):
        """
        读取临时文件内容
        :param tmp_file:  需要读取的临时文件
        :return: 临时文件内容
        """

        with open(tmp_file, "r") as f:
            tmp_content = f.read()

        return tmp_content

    def tmp_color_picfh(self, tmp_file, color):
        """
        解析tmp中带颜色的文字和它的前一项
        注意这个是表格形式,
        从这个文件解压而来PlcFFile
        :param tmp_file:  需要读取的临时文件
        :return: 字典格式 {key:value}
        "example" "":"on"
        """
        with open(tmp_file, "r",encoding="utf-8") as f:
            tmp_content = f.read()
        soup = BeautifulSoup(tmp_content, 'html.parser')
        # 获取包含颜色为 #00FF00 的字体元素
        font_elements = soup.find_all('font', {'color': color})

        # 用于存储结果的空字典
        result_dict = {}

        # 遍历字体元素，并获取相应的信息
        for font_element in font_elements:
            # 找到父级 td 元素
            td_element = font_element.parent

            # 找到包含 mess 值的元素
            mess_element = td_element.find_previous_sibling('td', {'id': 'mess'})

            # 获取 mess 和 b 的值
            mess_value = mess_element.get_text()
            b_value = font_element.get_text()

            # 将 mess ( b 的值组合成键值对，并添加到结果字典中
            result_dict[mess_value] = b_value
        # print(F"{len(result_dict)}--{result_dict}")
        return result_dict
    def tmp_blade_df(self, tmp_file):

        """
        读取临时文件，清理数据
        从这个文件解压而来PlcFFile
        :param tmp_file:  需要读取的临时文件
        :return: df 值

        """
        with open(tmp_file, 'r') as f:
            lines = f.readlines()
        # 去除前三行
        lines = lines[3:]

        # 获取表头
        header = lines.pop(0).strip().lstrip('#').split('; ')

        # 提取数据
        data = []
        for line in lines:
            data.append(line.strip().split(';'))

        # 转换为 DataFrame 对象
        df = pd.DataFrame(data, columns=header)
        # print(df.head(5))
        return  df

# if __name__ == '__main__':
#     tmp_path = R"../Temp/HistoryFile/2023/PlcFFile/tmp20230422/file20230422104746071.tmp"
#     color = "#00FF00"
#     TC = TmpCurd()
#     data = TC.tmp_color_picfh(tmp_path, color)
#     df = pd.DataFrame(list(data.items()))
#     df.to_csv('风机涡轮机错误信息.csv', index=False)
