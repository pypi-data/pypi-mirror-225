# -*- coding: utf-8 -*-
"""
@Time : 2023/6/23 23:17
@Author : sdb20200101@gmail.com
@File: RectangleRoi.py
@Software : PyCharm
"""

from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from .constant import keyMoveFactor


class RectangleRoi(QGraphicsRectItem):
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
        lt_x, lt_y, width, height = self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height()
        handle_width = 1 / self._scale_factor * 6

        self.left_top.setRect(QRectF(lt_x - handle_width / 2, lt_y - handle_width / 2, handle_width, handle_width))
        self.left_middle.setRect(
            QRectF(lt_x - handle_width / 2, lt_y + height / 2 - handle_width / 2, handle_width, handle_width))
        self.left_bottom.setRect(
            QRectF(lt_x - handle_width / 2, lt_y + height - handle_width / 2, handle_width, handle_width))
        self.middle_top.setRect(
            QRectF(lt_x + width / 2 - handle_width / 2, lt_y - handle_width / 2, handle_width, handle_width))
        self.middle_bottom.setRect(
            QRectF(lt_x + width / 2 - handle_width / 2, lt_y + height - handle_width / 2, handle_width, handle_width))
        self.right_top.setRect(
            QRectF(lt_x + width - handle_width / 2, lt_y - handle_width / 2, handle_width, handle_width))
        self.right_middle.setRect(
            QRectF(lt_x + width - handle_width / 2, lt_y + height / 2 - handle_width / 2, handle_width, handle_width))
        self.right_bottom.setRect(
            QRectF(lt_x + width - handle_width / 2, lt_y + height - handle_width / 2, handle_width, handle_width))

    def setROI(self, x: float, y: float, w: float, h: float):
        super().setRect(x, y, w, h)
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
        if self.contains(pos) and not self.is_handle(pos):
            return True

        return False

    def move_handle(self, pos: QPointF, index, start_pos: QPointF, init_point: list):
        x, y, w, h = self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height()
        x1, y1 = x + w, y + h
        if index == 1:
            x = pos.x()
            y = pos.y()
            w = x1 - x
            h = y1 - y
        elif index == 2:
            y = pos.y()
            h = y1 - y
        elif index == 3:
            y = pos.y()
            w = pos.x() - x
            h = y1 - y
        elif index == 4:
            x = pos.x()
            w = x1 - x
        elif index == 5:
            w = pos.x() - x
        elif index == 6:
            x = pos.x()
            w = x1 - x
            h = pos.y() - y
        elif index == 7:
            h = pos.y() - y
        elif index == 8:
            w = pos.x() - x
            h = pos.y() - y

        self.setRect(x, y, w, h)
        self.update_handles()

    def center(self):
        return [self.rect().center().x(), self.rect().center().y()]

    def move_roi(self, pos: QPointF, start_pos: QPointF, init_point: list):
        dx = pos.x() - start_pos.x()
        dy = pos.y() - start_pos.y()
        w = self.rect().width()
        h = self.rect().height()
        x = init_point[0] - w / 2 + dx
        y = init_point[1] - h / 2 + dy
        self.setRect(x, y, w, h)
        self.update_handles()

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
