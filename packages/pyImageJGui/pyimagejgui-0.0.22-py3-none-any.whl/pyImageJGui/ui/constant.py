# -*- coding: utf-8 -*-
"""
@Time : 2023/6/23 23:40
@Author : sdb20200101@gmail.com
@File: constant.py
@Software : PyCharm
"""
import enum


class ROI(enum.Enum):
    Rectangle = 1
    Circle = 2
    Polygon = 3
    Freehand = 4
    Line = 5
    Angle = 6
    Magnifier = 7
    Hand = 8
    Ellipse = 9
    Rotate = 10
    Save = 11


keyMoveFactor = 1
