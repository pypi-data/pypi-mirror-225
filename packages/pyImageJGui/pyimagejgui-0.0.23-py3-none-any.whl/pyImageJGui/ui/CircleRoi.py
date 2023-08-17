# -*- coding: utf-8 -*-
"""
@Time : 2023/7/22 10:14
@Author : sdb20200101@gmail.com
@File: CircleRoi.py
@Software : PyCharm
"""
import math
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from .constant import keyMoveFactor


class CircleRoi(QGraphicsEllipseItem):
    def __init__(self, scale_factor):
        super().__init__()
        self.left_top = QGraphicsRectItem()
        self.middle_top = QGraphicsRectItem()
        self.right_top = QGraphicsRectItem()
        self.left_middle = QGraphicsRectItem()
        self.right_middle = QGraphicsRectItem()
        self.left_bottom = QGraphicsRectItem()
        self.middle_bottom = QGraphicsRectItem()
        self.right_bottom = QGraphicsRectItem()
        self._scale_factor = scale_factor
        self.handle_brush = QBrush(Qt.GlobalColor.white)
        self.handle_pen = QPen(Qt.GlobalColor.black)
        self.handle_pen.setWidthF(1 / self._scale_factor)

        self.setBrush(QBrush(Qt.GlobalColor.transparent))
        self.pen = QPen(Qt.GlobalColor.yellow)
        self.pen.setWidthF(1 / self._scale_factor)
        self.setPen(self.pen)

        self.handles = [self.left_top, self.middle_top, self.right_top, self.left_middle, self.right_middle,
                        self.left_bottom, self.middle_bottom, self.right_bottom]

        for handle in self.handles:
            handle.setBrush(self.handle_brush)
            handle.setPen(self.handle_pen)

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
        self.scene().addItem(self.left_top)
        self.scene().addItem(self.left_middle)
        self.scene().addItem(self.left_bottom)
        self.scene().addItem(self.middle_top)
        self.scene().addItem(self.middle_bottom)
        self.scene().addItem(self.right_top)
        self.scene().addItem(self.right_middle)
        self.scene().addItem(self.right_bottom)

    def update_handles(self):
        handle_width = 1 / self._scale_factor * 6

        left_top_point = self.get_handle_point(135)
        self.left_top.setRect(
            QRectF(left_top_point[0] - handle_width / 2, left_top_point[1] - handle_width / 2, handle_width,
                   handle_width))

        left_middle_point = self.get_handle_point(180)
        self.left_middle.setRect(
            QRectF(left_middle_point[0] - handle_width / 2, left_middle_point[1] - handle_width / 2, handle_width,
                   handle_width))

        left_bottom_point = self.get_handle_point(225)
        self.left_bottom.setRect(
            QRectF(left_bottom_point[0] - handle_width / 2, left_bottom_point[1] - handle_width / 2, handle_width,
                   handle_width))

        middle_top_point = self.get_handle_point(90)
        self.middle_top.setRect(
            QRectF(middle_top_point[0] - handle_width / 2, middle_top_point[1] - handle_width / 2, handle_width,
                   handle_width))

        middle_bottom_point = self.get_handle_point(270)
        self.middle_bottom.setRect(
            QRectF(middle_bottom_point[0] - handle_width / 2, middle_bottom_point[1] - handle_width / 2, handle_width,
                   handle_width))

        right_top_point = self.get_handle_point(45)
        self.right_top.setRect(
            QRectF(right_top_point[0] - handle_width / 2, right_top_point[1] - handle_width / 2, handle_width,
                   handle_width))

        right_middle_point = self.get_handle_point(0)
        self.right_middle.setRect(
            QRectF(right_middle_point[0] - handle_width / 2, right_middle_point[1] - handle_width / 2, handle_width,
                   handle_width))

        right_bottom_point = self.get_handle_point(315)
        self.right_bottom.setRect(
            QRectF(right_bottom_point[0] - handle_width / 2, right_bottom_point[1] - handle_width / 2, handle_width,
                   handle_width))

    def setROI(self, x: float, y: float, r: float):
        x = x - r
        y = y - r
        w = 2 * r
        h = 2 * r
        super().setRect(x, y, w, h)
        self.update_handles()

    def get_handle_point(self, angle):
        cx = self.rect().center().x()
        cy = self.rect().center().y()
        a = self.rect().width() / 2
        b = self.rect().height() / 2
        radian = angle * math.pi / 180.0
        x = cx + a * math.cos(radian)
        y = cy + b * math.sin(radian)
        return [x, y]

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
        if self.contains(pos) and not self.is_handle(pos):
            return True

        return False

    def move_handle(self, pos: QPointF, index, start_pos: QPointF, init_point: list):
        cx = self.rect().center().x()
        cy = self.rect().center().y()
        r = math.sqrt((pos.x() - cx) ** 2 + (pos.y() - cy) ** 2)
        self.setROI(cx, cy, r)

    def move_roi(self, pos: QPointF, start_pos: QPointF, init_point: list):
        dx = pos.x() - start_pos.x()
        dy = pos.y() - start_pos.y()
        r = self.rect().width() / 2
        cx = init_point[0] + dx
        cy = init_point[1] + dy
        self.setROI(cx, cy, r)

    def center(self):
        return [self.rect().center().x(), self.rect().center().y()]

    def keyMove(self, event: QKeyEvent):
        d = 1 / self._scale_factor * keyMoveFactor
        x = self.rect().center().x()
        y = self.rect().center().y()
        r = self.rect().width() / 2
        if event.key() == Qt.Key.Key_Up:
            self.setROI(x, y - d, r)
        elif event.key() == Qt.Key.Key_Down:
            self.setROI(x, y + d, r)
        elif event.key() == Qt.Key.Key_Left:
            self.setROI(x - d, y, r)
        elif event.key() == Qt.Key.Key_Right:
            self.setROI(x + d, y, r)

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        super().paint(painter, option, widget)
