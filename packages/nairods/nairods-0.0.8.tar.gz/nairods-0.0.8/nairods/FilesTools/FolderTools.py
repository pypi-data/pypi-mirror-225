#! /usr/bin/env python
# -*-coding:utf-8-*-
import os


# 文件夹的增删改查
class FolderCurd(object):
    """
    文件夹操作
    """

    def __init__(self):
        pass

    def creat_folder(self, folder_path=""):
        """
        文件夹不存在则创建
        :param folder_path: 文件夹地址
        :return: 创建成功
        """

        if not os.path.exists(os.path.dirname(folder_path)):
            try:
                os.makedirs(os.path.dirname(folder_path))
                return "创建成功"
            except OSError as exc:
                raise exc

    def walk_folder_path(self, destination_folder=""):
        """
        遍历目标文件夹下的所有文件
        :param destination_folder:  目标文件夹
        :return: 文件列表
        """

        # 递归遍历当前目录及其子目录下的所有文件
        result = {}
        for root, dirs, files in os.walk(destination_folder):
            files_list = [os.path.join(root, file) for file in files]
            if files_list:
                result[root] = files_list

        return result

    def save_latest_files(self, folder_path):
        """
        保留文件夹下最新的文件
        :param folder_path:  目标文件夹
        :return: F'已保留最新文件'
        """
        # 获取目录下所有文件及它们的属性
        files_list = [(f, os.path.getmtime(os.path.join(folder_path, f))) for f in os.listdir(folder_path)]

        # 根据修改时间（即最后一次保存时间）对文件列表进行排序
        sorted_files = sorted(files_list, key=lambda x: x[1])

        # 删除修改时间较早的文件
        for file, modified_time in sorted_files[:-1]:
            os.remove(os.path.join(folder_path, file))

        return F'已保留最新文件'

# if __name__ == '__main__':
#     local_folder_path = F'..\\Temp\\HistoryFile\\2023\\'  # 本地保存文件路径,使用os.sep
#     FC =FolderCurd()
#     FC.walk_folder_path(local_folder_path)
