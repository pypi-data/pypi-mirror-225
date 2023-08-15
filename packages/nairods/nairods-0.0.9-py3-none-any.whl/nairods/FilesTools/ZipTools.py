#! /usr/bin/env python
# -*-coding:utf-8-*-
import zipfile
from nairods.FileTools.FolderTools import FolderCurd


# 压缩文件的增删改查等
class ZipCurd(object):
    """
    arc文件操作
    """

    def __init__(self, zip_path=""):
        self.zip_path = zip_path

    def unzip_file(self, zip_file, save_folder):
        """
        解压文件到指定文件夹
        :param zip_file:  需要解压的文件
        :param save_folder:    保存的本地文件夹
        :return: 保存成功
        """
        FC = FolderCurd()
        FC.creat_folder(save_folder)
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(save_folder)
        return "解压成功"



# if __name__ == '__main__':
#     ZC = ZipCurd()

