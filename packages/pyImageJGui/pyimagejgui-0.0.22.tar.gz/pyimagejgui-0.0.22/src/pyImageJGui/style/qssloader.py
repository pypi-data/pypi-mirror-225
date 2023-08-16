# -*- coding: utf-8 -*-
"""
@Time : 2023/6/22 13:42
@Author : sdb20200101@gmail.com
@File: qssloader.py
@Software : PyCharm
"""
import os

path = os.path.dirname(__file__)


class QSSLoader(object):
    def __init__(self):
        pass

    @staticmethod
    def read_qss_file(qss_file_name):
        with open(qss_file_name, 'r', encoding='UTF-8') as file:
            return file.read()


style = QSSLoader.read_qss_file(os.path.join(path, "main.qss"))
