# -*- coding: utf-8 -*-
"""
@Time : 2023/7/30 12:49
@Author : sdb20200101@gmail.com
@File: icon.py
@Software : PyCharm
"""
import qt_material
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *


def oval_icon(size: QSize):
    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)

    pen_color = Qt.GlobalColor.black
    pen_width = size.width() / 15
    pen = QPen(pen_color)
    pen.setWidthF(pen_width)

    brush = QBrush(Qt.GlobalColor.transparent)

    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(pen)
    painter.setBrush(brush)

    painter.drawEllipse(pen_width, pen_width, size.width() - pen_width * 2 - 1, size.height() - pen_width * 2 - 1)

    painter.end()

    return pixmap


def rectangle_icon(size: QSize):
    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)

    pen_color = Qt.GlobalColor.black
    pen_width = size.width() / 15
    pen = QPen(pen_color)
    pen.setWidthF(pen_width)

    brush = QBrush(Qt.GlobalColor.transparent)

    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(pen)
    painter.setBrush(brush)

    painter.drawRect(pen_width, pen_width, size.width() - pen_width * 2 - 1, size.height() - pen_width * 2 - 1)

    painter.end()

    return pixmap


def line_icon(size: QSize):
    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)

    pen_color = Qt.GlobalColor.black
    pen_width = size.width() / 15
    pen = QPen(pen_color)
    pen.setWidthF(pen_width)

    brush = QBrush(Qt.GlobalColor.transparent)

    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(pen)
    painter.setBrush(brush)

    painter.drawLine(QPointF(pen_width, size.height() - pen_width - 1),
                     QPointF(size.width() - pen_width - 1, pen_width))

    painter.end()

    return pixmap


def angle_icon(size: QSize):
    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)

    pen_color = Qt.GlobalColor.black
    pen_width = size.width() / 15
    pen = QPen(pen_color)
    pen.setWidthF(pen_width)

    brush = QBrush(Qt.GlobalColor.transparent)

    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(pen)
    painter.setBrush(brush)

    painter.drawLine(QPointF(pen_width, size.height() - pen_width - 1),
                     QPointF(size.width() - pen_width - 1, pen_width))
    painter.drawLine(QPointF(pen_width, size.height() - pen_width - 1),
                     QPointF(size.width() - pen_width - 1, size.height() - pen_width - 1))

    painter.end()

    return pixmap


def clear_icon(size: QSize):
    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)

    pen_color = Qt.GlobalColor.black
    pen_width = size.width() / 15
    pen = QPen(pen_color)
    pen.setWidthF(pen_width)

    brush = QBrush(Qt.GlobalColor.transparent)

    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(pen)
    painter.setBrush(brush)

    painter.drawLine(QPointF(pen_width * 2, size.height() - pen_width * 2 - 1),
                     QPointF(size.width() - pen_width * 2 - 1, pen_width * 2))
    painter.drawLine(QPointF(pen_width * 2, pen_width * 2),
                     QPointF(size.width() - pen_width * 2 - 1, size.height() - pen_width * 2 - 1))

    painter.end()

    return pixmap


def hand_icon(size: QSize):
    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)

    pen_color = Qt.GlobalColor.black
    pen_width = size.width() / 15
    pen = QPen(pen_color)
    pen.setWidthF(pen_width)

    brush = QBrush(Qt.GlobalColor.transparent)

    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(pen)
    painter.setBrush(brush)

    painter.drawLine(size.height() / 2, pen_width, size.height() / 2, size.width() - pen_width - 1)

    painter.drawLine(pen_width, size.width() / 2, size.height() - pen_width - 1, size.width() / 2)

    painter.end()

    return pixmap
