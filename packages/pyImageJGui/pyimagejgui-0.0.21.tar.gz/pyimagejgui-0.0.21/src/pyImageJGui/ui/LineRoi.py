# -*- coding: utf-8 -*-
"""
@Time : 2023/7/22 23:56
@Author : sdb20200101@gmail.com
@File: LineRoi.py
@Software : PyCharm
"""
import math

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from .constant import keyMoveFactor


class LineRoi(QGraphicsLineItem):
    def __init__(self, scale_factor):
        super().__init__()
        self.start = QGraphicsRectItem()
        self.end = QGraphicsRectItem()
        self.middle = QGraphicsRectItem()

        self._scale_factor = scale_factor
        self.handle_brush = QBrush(Qt.GlobalColor.white)
        self.handle_pen = QPen(Qt.GlobalColor.black)
        self.handle_pen.setWidthF(1 / self._scale_factor)

        self.pen = QPen(Qt.GlobalColor.yellow)
        self.pen.setWidthF(1 / self._scale_factor)
        self.setPen(self.pen)

        self.handles = [self.start, self.end, self.middle]

        for handle in self.handles:
            handle.setBrush(self.handle_brush)
            handle.setPen(self.handle_pen)

        self.start.setBrush(Qt.GlobalColor.yellow)

    @property
    def scale_factor(self):
        return self._scale_factor

    @scale_factor.setter
    def scale_factor(self, value):
        self._scale_factor = value
        self.handle_pen.setWidthF(1 / self._scale_factor)
        self.pen.setWidthF(1 / self._scale_factor)

        for handle in self.handles:
            handle.setPen(self.handle_pen)

        self.update_handles()

        self.setPen(self.pen)

    def set_handles(self):
        self.scene().addItem(self.start)
        self.scene().addItem(self.end)
        self.scene().addItem(self.middle)

    def update_handles(self):
        handle_width = 1 / self._scale_factor * 6

        start_point = self.line().p1()
        self.start.setRect(
            QRectF(start_point.x() - handle_width / 2, start_point.y() - handle_width / 2, handle_width,
                   handle_width))

        end_point = self.line().p2()
        self.end.setRect(
            QRectF(end_point.x() - handle_width / 2, end_point.y() - handle_width / 2, handle_width,
                   handle_width))

        middle_point = self.line().center()
        self.middle.setRect(
            QRectF(middle_point.x() - handle_width / 2, middle_point.y() - handle_width / 2, handle_width,
                   handle_width))

    def setROI(self, x1: float, y1: float, x2: float, y2: float):
        super().setLine(x1, y1, x2, y2)
        self.update_handles()

    def clear_from_scene(self, scene: QGraphicsScene):
        scene.removeItem(self)
        for handle in self.handles:
            scene.removeItem(handle)

    def is_handle(self, pos: QPointF):
        for index, handle in enumerate(self.handles):
            if handle.contains(pos):
                return index + 1

        return None

    def is_in_roi(self, pos: QPointF):
        return False

    def move_handle(self, pos: QPointF, index, start_pos: QPointF, init_point: list):
        p1_x = self.line().x1()
        p1_y = self.line().y1()
        p2_x = self.line().center().x()
        p2_y = self.line().center().y()
        p3_x = self.line().x2()
        p3_y = self.line().y2()
        if index == 1:
            p1_x = pos.x()
            p1_y = pos.y()
        elif index == 2:
            p3_x = pos.x()
            p3_y = pos.y()
        elif index == 3:
            dx = pos.x() - p2_x
            dy = pos.y() - p2_y
            p1_x = p1_x + dx
            p1_y = p1_y + dy
            p3_x = p3_x + dx
            p3_y = p3_y + dy

        self.setROI(p1_x, p1_y, p3_x, p3_y)

    def move_roi(self, pos: QPointF, start_pos: QPointF, init_point: list):
        pass

    def center(self):
        return [self.line().center().x(), self.line().center().y()]

    def keyMove(self, event: QKeyEvent):
        d = 1 / self._scale_factor * keyMoveFactor
        x1 = self.line().x1()
        y1 = self.line().y1()
        x2 = self.line().x2()
        y2 = self.line().y2()
        if event.key() == Qt.Key.Key_Up:
            self.setROI(x1, y1 - d, x2, y2 - d)
        elif event.key() == Qt.Key.Key_Down:
            self.setROI(x1, y1 + d, x2, y2 + d)
        elif event.key() == Qt.Key.Key_Left:
            self.setROI(x1 - d, y1, x2 - d, y2)
        elif event.key() == Qt.Key.Key_Right:
            self.setROI(x1 + d, y1, x2 + d, y2)

    def paint(self, painter, option, widget):
        if self.line().angle() not in [0, 90, 180, 270]:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        super().paint(painter, option, widget)
