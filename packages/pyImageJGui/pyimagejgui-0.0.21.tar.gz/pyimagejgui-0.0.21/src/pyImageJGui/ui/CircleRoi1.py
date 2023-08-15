# -*- coding: utf-8 -*-
"""
@Time : 2023/8/12 03:18
@Author : sdb20200101@gmail.com
@File: CircleRoi1.py
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
        self.middle_top = QGraphicsRectItem()
        self.left_middle = QGraphicsRectItem()
        self.right_middle = QGraphicsRectItem()
        self.middle_bottom = QGraphicsRectItem()
        self._scale_factor = scale_factor
        self.handle_brush = QBrush(Qt.GlobalColor.white)
        self.handle_pen = QPen(Qt.GlobalColor.black)
        self.handle_pen.setWidthF(1 / self._scale_factor)

        self.setBrush(QBrush(Qt.GlobalColor.transparent))
        self.pen = QPen(Qt.GlobalColor.yellow)
        self.pen.setWidthF(1 / self._scale_factor)
        self.setPen(self.pen)

        self.handles = [self.middle_top, self.left_middle, self.right_middle, self.middle_bottom]

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
        self.scene().addItem(self.left_middle)
        self.scene().addItem(self.middle_top)
        self.scene().addItem(self.middle_bottom)
        self.scene().addItem(self.right_middle)

    def update_handles(self):
        handle_width = 1 / self._scale_factor * 6

        left_middle_point = self.get_handle_point(180)
        self.left_middle.setRect(
            QRectF(left_middle_point[0] - handle_width / 2, left_middle_point[1] - handle_width / 2, handle_width,
                   handle_width))

        middle_top_point = self.get_handle_point(270)
        self.middle_top.setRect(
            QRectF(middle_top_point[0] - handle_width / 2, middle_top_point[1] - handle_width / 2, handle_width,
                   handle_width))

        middle_bottom_point = self.get_handle_point(90)
        self.middle_bottom.setRect(
            QRectF(middle_bottom_point[0] - handle_width / 2, middle_bottom_point[1] - handle_width / 2, handle_width,
                   handle_width))

        right_middle_point = self.get_handle_point(0)
        self.right_middle.setRect(
            QRectF(right_middle_point[0] - handle_width / 2, right_middle_point[1] - handle_width / 2, handle_width,
                   handle_width))

    def setROI(self, x: float, y: float, w: float, h: float):
        super().setRect(x, y, w, w)
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
        dx = pos.x() - start_pos.x()
        dy = pos.y() - start_pos.y()
        x, y, w, h = init_point[0], init_point[1], init_point[2], init_point[3]
        x1, y1 = x + w, y + h
        if index == 1:
            y = y + dy
            h = y1 - y
            w = h
        elif index == 2:
            x = x + dx
            w = x1 - x
            h = w
        elif index == 3:
            w = w + dx
            h = w
        elif index == 4:
            h = h + dy
            w = h

        self.setRect(x, y, w, h)
        self.update_handles()

    def move_roi(self, pos: QPointF, start_pos: QPointF, init_point: list):
        dx = pos.x() - start_pos.x()
        dy = pos.y() - start_pos.y()
        x = init_point[0] + dx
        y = init_point[1] + dy
        w = self.rect().width()
        h = self.rect().height()
        self.setROI(x, y, w, h)

    def center(self):
        return [self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height()]

    def keyMove(self, event: QKeyEvent):
        d = 1 / self._scale_factor * keyMoveFactor
        x = self.rect().x()
        y = self.rect().y()
        w = self.rect().width()
        h = self.rect().height()
        if event.key() == Qt.Key.Key_Up:
            self.setROI(x, y - d, w, h)
        elif event.key() == Qt.Key.Key_Down:
            self.setROI(x, y + d, w, h)
        elif event.key() == Qt.Key.Key_Left:
            self.setROI(x - d, y, w, h)
        elif event.key() == Qt.Key.Key_Right:
            self.setROI(x + d, y, w, h)

    def get_rect(self):
        x = self.rect().x()
        y = self.rect().y()
        w = self.rect().width()
        h = self.rect().height()
        if w < 0 and h < 0:
            x = x + w
            y = y + h
            w = -w
            h = -h
        elif w > 0 > h:
            y = y + h
            h = -h
        elif h > 0 > w:
            x = x + w
            w = -w
        return QRectF(x, y, w, h)

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        super().paint(painter, option, widget)
