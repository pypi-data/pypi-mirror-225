#! /usr/bin/env python
# -*-coding:utf-8-*-

import yaml
import os
import sys

# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 将该目录加入系统路径中，这样 Python 解释器就能找到 'FileTools' 模块
sys.path.insert(0, os.path.join(current_dir, '..'))
# yml增删改查
class YmlCurd(object):
    """
    yml操作
    """

    def __init__(self, yml_path=""):
        self.yml_path = yml_path

    def read_yaml(self):
        """
        读取yml文件
        :return: 全部数据,为字典
        """
        with open(self.yml_path, 'r') as f:

            result = yaml.safe_load(f)
        print(result)
        return result


# if __name__ == '__main__':
# #     YC = YmlCurd(R"demo_20230418.yml")
#     YC = YmlCurd("../ConfigTools/DatabaseConfig/SanquServe.yml")
#     YC.read_yaml()
