#! /usr/bin/env python
# -*-coding:utf-8-*-
import pandas as pd
import xlwt

# excle的增删改查
class Excle_Curd(object):
    """
    excle操作
    """

    def __init__(self, excle_path=""):
        self.excle_path = excle_path

    def read_excle(self):
        """
        读取excle文件
        :return: 全部数据,为字典
        """
        result = pd.read_excel(self.excle_path, header=0, keep_default_na=False).values
        return result

    def save_list_excle(self, title, result_li, save_name, sheet="sheet1"):
        """
        列表保存到表格
        :param res_li: 获得的列表值
        :param save_t_name: 保存的文件名称
        :param save_t_name: 表格的第一个窗口名

        :return: 保存的文件名称
        """

        book = xlwt.Workbook()
        sheet = book.add_sheet(sheet)

        for i, t in enumerate(title):
            sheet.write(0, i, t)
        for i, d in enumerate(result_li):
            for j, one in enumerate(d):
                sheet.write(0, i * len(d) + j, one)

        book.save(f"{save_name}.xls")
        return save_name


# if __name__ == '__main__':
#     EC = Excle_Curd(R"demo_20230418.yml")
#     EC.read_excle()
