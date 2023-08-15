# -*- coding: utf-8 -*-
"""
@Time : 2023/7/29 03:33
@Author : sdb20200101@gmail.com
@File: function.py
@Software : PyCharm
"""
import os
import cv2 as cv
import numpy as np
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *


def imread(file_path, dtype=np.uint8):
    img = cv.imdecode(np.fromfile(file_path, dtype=dtype), 0)
    return img


def imwrite(save_path, img, format='bmp'):
    cv.imencode('.' + format, img)[1].tofile(save_path)


def save_pixmap(save_path, pixmap: QPixmap, format='bmp'):
    arr = QPixmapToArray(pixmap)
    imwrite(save_path, arr, format)


def show_message_box(text):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Information)
    msg_box.setText(text)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.exec()


def QPixmapToArray(qpix: QPixmap):
    qimage = qpix.toImage()

    size = qimage.size()
    width = size.width()
    height = size.height()
    depth = qimage.depth()

    buffer = qimage.constBits()
    arr = np.frombuffer(buffer, dtype=np.uint8).reshape((height, width, depth // 8))
    arr = arr[:, :, 0]
    return arr
