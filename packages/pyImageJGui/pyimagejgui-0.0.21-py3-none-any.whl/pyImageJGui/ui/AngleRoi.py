# -*- coding: utf-8 -*-
"""
@Time : 2023/7/23 00:12
@Author : sdb20200101@gmail.com
@File: AngleRoi.py
@Software : PyCharm
"""
from typing import Union

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from .LineRoi import LineRoi
from shapely import geometry
from .constant import keyMoveFactor


class AngleRoi():
    def __init__(self, scale_factor):
        self.line1 = LineRoi(scale_factor)
        self.line2 = LineRoi(scale_factor)

        self.p1 = QGraphicsRectItem()
        self.p2 = QGraphicsRectItem()
        self.p3 = QGraphicsRectItem()

        self._scale_factor = scale_factor

        self.handle_brush = QBrush(Qt.GlobalColor.white)
        self.handle_pen = QPen(Qt.GlobalColor.black)
        self.handle_pen.setWidthF(1 / self._scale_factor)

        self.line_pen = QPen(Qt.GlobalColor.yellow)
        self.line_pen.setWidthF(1 / self._scale_factor)

        self.handles = [self.p1, self.p2, self.p3]

        for handle in self.handles:
            handle.setBrush(self.handle_brush)
            handle.setPen(self.handle_pen)

        self.p1.setBrush(Qt.GlobalColor.yellow)

    @property
    def scale_factor(self):
        return self._scale_factor

    @scale_factor.setter
    def scale_factor(self, value):
        self._scale_factor = value

        self.handle_pen.setWidthF(1 / self._scale_factor)
        self.line_pen.setWidthF(1 / self._scale_factor)

        for handle in self.handles:
            handle.setPen(self.handle_pen)

        self.update_line1_handles()

        self.update_line2_handles()

        self.line1.setPen(self.line_pen)
        self.line2.setPen(self.line_pen)

    def set_handles(self):
        pass

    def update_line1_handles(self):
        handle_width = 1 / self._scale_factor * 6

        start_point = self.line1.line().p1()
        self.p1.setRect(
            QRectF(start_point.x() - handle_width / 2, start_point.y() - handle_width / 2, handle_width,
                   handle_width))

        end_point = self.line1.line().p2()
        self.p2.setRect(
            QRectF(end_point.x() - handle_width / 2, end_point.y() - handle_width / 2, handle_width,
                   handle_width))

    def update_line2_handles(self):
        handle_width = 1 / self._scale_factor * 6

        start_point = self.line2.line().p1()
        self.p2.setRect(
            QRectF(start_point.x() - handle_width / 2, start_point.y() - handle_width / 2, handle_width,
                   handle_width))

        end_point = self.line2.line().p2()
        self.p3.setRect(
            QRectF(end_point.x() - handle_width / 2, end_point.y() - handle_width / 2, handle_width,
                   handle_width))

    def add_to_scene(self, scene: QGraphicsScene):
        scene.addItem(self.line1)
        scene.addItem(self.line2)
        for handle in self.handles:
            scene.addItem(handle)

    def clear_from_scene(self, scene: QGraphicsScene):
        scene.removeItem(self.line1)
        scene.removeItem(self.line2)
        for handle in self.handles:
            scene.removeItem(handle)

    def setROI(self, x: float, y: float, index: int, key: Union[Qt.Key, None]):
        if index == 1:
            self.line1.setROI(x, y, x, y)
        elif index == 2:
            point1_x = self.line1.line().p1().x()
            point1_y = self.line1.line().p1().y()
            if key == Qt.Key.Key_Shift:
                dx = abs(x - point1_x)
                dy = abs(y - point1_y)
                if dx >= dy:
                    y = point1_y
                else:
                    x = point1_x
            self.line1.setROI(point1_x, point1_y, x, y)
            self.line2.setROI(x, y, x, y)
        elif index == 3:
            point2_x = self.line1.line().p2().x()
            point2_y = self.line1.line().p2().y()
            if key == Qt.Key.Key_Shift:
                dx = abs(x - point2_x)
                dy = abs(y - point2_y)
                if dx >= dy:
                    y = point2_y
                else:
                    x = point2_x
            self.line2.setROI(point2_x, point2_y, x, y)

        self.update_line1_handles()
        self.update_line2_handles()

    def setTotalROI(self, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float):
        self.line1.setROI(x1, y1, x2, y2)
        self.line2.setROI(x2, y2, x3, y3)
        self.update_line1_handles()
        self.update_line2_handles()

    def is_handle(self, pos: QPointF):
        for index, handle in enumerate(self.handles):
            if handle.contains(pos):
                return index + 1

        return None

    def is_in_roi(self, pos: QPointF):
        p1 = (self.p1.rect().center().x(), self.p1.rect().center().y())
        p2 = (self.p2.rect().center().x(), self.p2.rect().center().y())
        p3 = (self.p3.rect().center().x(), self.p3.rect().center().y())
        triangle = geometry.Polygon([p1, p2, p3])
        p = geometry.Point([pos.x(), pos.y()])
        return triangle.contains(p) and not self.is_handle(pos)

    def move_handle(self, pos: QPointF, index, start_pos: QPointF, init_point: list):
        if index == 1:
            self.line1.setROI(pos.x(), pos.y(), self.line1.line().p2().x(), self.line1.line().p2().y())
        elif index == 2:
            self.line1.setROI(self.line1.line().p1().x(), self.line1.line().p1().y(), pos.x(), pos.y())
            self.line2.setROI(pos.x(), pos.y(), self.line2.line().p2().x(), self.line2.line().p2().y())
        elif index == 3:
            self.line2.setROI(self.line2.line().p1().x(), self.line2.line().p1().y(), pos.x(), pos.y())

        self.update_line1_handles()
        self.update_line2_handles()

    def move_roi(self, pos: QPointF, start_pos: QPointF, init_point: list):
        dx = pos.x() - start_pos.x()
        dy = pos.y() - start_pos.y()
        p1_x = init_point[0] + dx
        p1_y = init_point[1] + dy
        p2_x = init_point[2] + dx
        p2_y = init_point[3] + dy
        p3_x = init_point[4] + dx
        p3_y = init_point[5] + dy
        self.setTotalROI(p1_x, p1_y, p2_x, p2_y, p3_x, p3_y)

    def get_angle(self):
        angle1 = self.line1.line().angle()
        angle2 = self.line2.line().angle()
        return abs(angle2 - angle1)

    def get_corner_point(self):
        p1 = self.line1.line().p1()
        p2 = self.line1.line().p2()
        p3 = self.line2.line().p2()
        return [p1.x(), p1.y(), p2.x(), p2.y(), p3.x(), p3.y()]

    def keyMove(self, event: QKeyEvent):
        d = 1 / self._scale_factor * keyMoveFactor
        p1_x = self.line1.line().x1()
        p1_y = self.line1.line().y1()
        p2_x = self.line1.line().x2()
        p2_y = self.line1.line().y2()
        p3_x = self.line2.line().x2()
        p3_y = self.line2.line().y2()
        if event.key() == Qt.Key.Key_Up:
            self.setTotalROI(p1_x, p1_y - d, p2_x, p2_y - d, p3_x, p3_y - d)
        elif event.key() == Qt.Key.Key_Down:
            self.setTotalROI(p1_x, p1_y + d, p2_x, p2_y + d, p3_x, p3_y + d)
        elif event.key() == Qt.Key.Key_Left:
            self.setTotalROI(p1_x - d, p1_y, p2_x - d, p2_y, p3_x - d, p3_y)
        elif event.key() == Qt.Key.Key_Right:
            self.setTotalROI(p1_x + d, p1_y, p2_x + d, p2_y, p3_x + d, p3_y)
