# -*- coding: utf-8 -*-
"""
@Time : 2023/6/22 00:10
@Author : sdb20200101@gmail.com
@File: gui.py
@Software : PyCharm
"""
import math
import os

import numpy as np
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import cv2 as cv
from .imageView import ImageViewer
from .constant import ROI
from ..utils.function import *
from .RectangleRoi import RectangleRoi
from .CircleRoi import CircleRoi
from .LineRoi import LineRoi
from .AngleRoi import AngleRoi
from .EllipseRoi import EllipseRoi
from ..icon.icon import *
import qtawesome as qta

path = os.path.dirname(os.path.dirname(__file__))


class ImageWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.layout = QVBoxLayout(self)
        self.button_layout = QHBoxLayout()

        self.last_open_dir = '/Users/sdb/image'
        self.roi = ROI.Hand

        icon_size = 20
        size = QSize(icon_size, icon_size)
        self.rectangle_button = Button(rectangle_icon(QSize(icon_size * 100, icon_size * 90)), '', ROI.Rectangle)
        self.angle_button = Button(angle_icon(QSize(icon_size * 100, icon_size * 100)), '', ROI.Angle)
        self.circle_button = Button(oval_icon(QSize(icon_size * 100, icon_size * 100)), '', ROI.Circle)
        rotate_icon = qta.icon('msc.refresh')
        self.rotate_button = QPushButton(rotate_icon, '')
        self.rotate_button.setIconSize(size)
        self.line_button = Button(line_icon(QSize(icon_size * 100, icon_size * 100)), '', ROI.Line)
        self.ellipse_button = Button(oval_icon(QSize(icon_size * 100, icon_size * 90)), '', ROI.Ellipse)
        save_icon = qta.icon('msc.save')
        self.save_button = QPushButton(save_icon, '')
        self.save_button.setIconSize(size)
        hand_icon = qta.icon('ei.move')
        self.hand_button = Button(hand_icon, '', ROI.Hand)
        self.hand_button.setIconSize(size)
        self.hand_button.setEnabled(False)
        clear_icon = qta.icon('msc.clear-all')
        self.clear_button = QPushButton(clear_icon, '')
        self.clear_button.setIconSize(size)
        file_icon = qta.icon('msc.folder')
        self.file_button = QPushButton(file_icon, '')
        self.file_button.setIconSize(size)
        self.button_layout.addWidget(self.rectangle_button)
        self.button_layout.addWidget(self.circle_button)
        self.button_layout.addWidget(self.ellipse_button)
        self.button_layout.addWidget(self.line_button)
        self.button_layout.addWidget(self.angle_button)
        self.button_layout.addWidget(self.rotate_button)
        self.button_layout.addWidget(self.hand_button)
        self.button_layout.addWidget(self.clear_button)
        self.button_layout.addWidget(self.file_button)
        self.button_layout.addWidget(self.save_button)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setSpacing(0)
        self.button_layout.addStretch(30)

        self.information = QLineEdit()
        self.measure_btn = QPushButton("Measure")
        self.find_edge_btn = QPushButton("Find Edge")
        self.information_layout = QHBoxLayout()
        self.information_layout.addWidget(self.information)
        self.information_layout.addWidget(self.measure_btn)
        self.information_layout.addWidget(self.find_edge_btn)
        self.figure = ImageViewer(self.information, self.roi, self)
        self.layout.addLayout(self.button_layout, 10)
        self.layout.addLayout(self.information_layout, 10)
        self.layout.addWidget(self.figure, 80)

        self.file_button.clicked.connect(self.file_btn_click)
        self.clear_button.clicked.connect(self.clear_btn_click)
        self.measure_btn.clicked.connect(self.measure_btn_click)
        self.save_button.clicked.connect(self.save_btn_click)
        self.rotate_button.clicked.connect(self.rotate_btn_click)
        self.find_edge_btn.clicked.connect(self.find_edge_btn_click)
        self.btn_connect()

    def file_btn_click(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self,  # 父窗口对象
            "选择存储路径",  # 标题
            self.last_open_dir  # 起始目录
        )
        self.last_open_dir = os.path.dirname(filePath)
        if filePath:
            img = imread(filePath)
            self.figure.setImageNoQImage(img)
            self.figure.setFocus()

    def btn_connect(self):
        buttons = self.findChildren(Button)
        for button in buttons:
            button.clicked.connect(self.roi_btn_click)

    def roi_btn_click(self):
        sender = self.sender()
        buttons = self.findChildren(Button)
        for button in buttons:
            if button.roi == self.roi:
                button.setEnabled(True)
        sender.setEnabled(False)
        self.roi = sender.roi
        self.figure.roi_state = self.roi

        if sender.roi == ROI.Hand:
            self.figure.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            self.figure.mouseMoveEvent = self.figure.mouseMoveEventNoRoi
            self.figure.mousePressEvent = self.figure.mousePressEventNoRoi
            self.figure.mouseReleaseEvent = self.figure.mouseReleaseEventNoRoi
        elif sender.roi == ROI.Rectangle or sender.roi == ROI.Circle or sender.roi == ROI.Line or sender.roi == ROI.Ellipse:
            self.figure.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.figure.mouseMoveEvent = self.figure.mouseMoveEventRoi
            self.figure.mousePressEvent = self.figure.mousePressEventRoi
            self.figure.mouseReleaseEvent = self.figure.mouseReleaseEventRoi
        elif sender.roi == ROI.Angle:
            self.figure.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.figure.mouseMoveEvent = self.figure.mouseMoveAngleEvent
            self.figure.mousePressEvent = self.figure.mousePressAngleEvent
            self.figure.mouseReleaseEvent = self.figure.mouseReleaseAngleEvent

    def clear_btn_click(self):
        self.figure.clear()

    def measure_btn_click(self):
        dialog = QDialog(self)
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.setWindowTitle("ROI Datas")
        dialog.setMinimumSize(QSize(900, 100))
        layout = QVBoxLayout(dialog)
        roi = self.figure.roi
        roi_table = QTableWidget()
        header = roi_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        roi_table.insertRow(roi_table.rowCount())
        layout.addWidget(roi_table)
        if isinstance(roi, RectangleRoi):
            roi_table.setColumnCount(7)
            roi_table.setHorizontalHeaderLabels(["Mean", "Min", "Max", "x", "y", "Width", "Height"])

            rect = roi.get_rect().toRect()

            pix_roi = self.figure.pixmap_item.pixmap().copy(rect)
            arr = QPixmapToArray(pix_roi)

            Mean = round(np.mean(arr), 3)
            Max = np.max(arr)
            Min = np.min(arr)

            x = rect.x()
            y = rect.y()
            width = rect.width()
            height = rect.height()

            roi_table.setItem(roi_table.rowCount() - 1, 0, QTableWidgetItem(str(Mean)))
            roi_table.setItem(roi_table.rowCount() - 1, 1, QTableWidgetItem(str(Min)))
            roi_table.setItem(roi_table.rowCount() - 1, 2, QTableWidgetItem(str(Max)))
            roi_table.setItem(roi_table.rowCount() - 1, 3, QTableWidgetItem(str(x)))
            roi_table.setItem(roi_table.rowCount() - 1, 4, QTableWidgetItem(str(y)))
            roi_table.setItem(roi_table.rowCount() - 1, 5, QTableWidgetItem(str(width)))
            roi_table.setItem(roi_table.rowCount() - 1, 6, QTableWidgetItem(str(height)))

            roi_copy_btn = QPushButton("Copy")
            layout.addWidget(roi_copy_btn)

            def roi_copy_btn_click():
                clipboard = QApplication.clipboard()
                clipboard.setText(str(x) + ' ' + str(y) + ' ' + str(width) + ' ' + str(height))
                QMessageBox.information(self, "Info", "Roi copied to clipboard!")

            roi_copy_btn.clicked.connect(roi_copy_btn_click)

        if isinstance(roi, CircleRoi):
            roi_table.setColumnCount(6)
            roi_table.setHorizontalHeaderLabels(["Mean", "Min", "Max", "cx", "cy", "Radius"])

            rect = roi.rect().toRect()

            pix_roi = self.figure.pixmap_item.pixmap().copy(rect)
            arr = QPixmapToArray(pix_roi)

            mask = np.zeros_like(arr)
            h, w = arr.shape[:2]
            center = (w // 2, h // 2)
            raduis = min(h, w) // 2
            cv.circle(mask, center, raduis, 255, -1)

            roi_masked = cv.bitwise_and(arr, arr, mask=mask)
            roi_masked = roi_masked[roi_masked > 0]

            Mean = round(np.mean(roi_masked), 3)
            Max = np.max(roi_masked)
            Min = np.min(roi_masked)

            cx = rect.x() + w // 2
            cy = rect.y() + h // 2

            roi_table.setItem(roi_table.rowCount() - 1, 0, QTableWidgetItem(str(Mean)))
            roi_table.setItem(roi_table.rowCount() - 1, 1, QTableWidgetItem(str(Min)))
            roi_table.setItem(roi_table.rowCount() - 1, 2, QTableWidgetItem(str(Max)))
            roi_table.setItem(roi_table.rowCount() - 1, 3, QTableWidgetItem(str(cx)))
            roi_table.setItem(roi_table.rowCount() - 1, 4, QTableWidgetItem(str(cy)))
            roi_table.setItem(roi_table.rowCount() - 1, 5, QTableWidgetItem(str(raduis)))

        if isinstance(roi, EllipseRoi):
            roi_table.setColumnCount(8)
            roi_table.setHorizontalHeaderLabels(["Mean", "Min", "Max", "Cx", "Cy", "Major", "Minor", "Ovality"])

            rect = roi.get_rect().toRect()
            cx = rect.center().x()
            cy = rect.center().y()
            major = rect.width()
            minor = rect.height()
            axis = [major, minor]
            ovality = round(abs(1 - min(axis) / max(axis)), 4)

            pix_roi = self.figure.pixmap_item.pixmap().copy(rect)
            arr = QPixmapToArray(pix_roi)

            mask = np.zeros_like(arr)
            h, w = arr.shape[:2]
            center = (w // 2, h // 2)

            cv.ellipse(mask, center, axis, 0, 0, 360, 255, -1)
            roi_masked = cv.bitwise_and(arr, arr, mask=mask)
            roi_masked = roi_masked[roi_masked > 0]

            Mean = round(np.mean(roi_masked), 3)
            Max = np.max(roi_masked)
            Min = np.min(roi_masked)

            roi_table.setItem(roi_table.rowCount() - 1, 0, QTableWidgetItem(str(Mean)))
            roi_table.setItem(roi_table.rowCount() - 1, 1, QTableWidgetItem(str(Min)))
            roi_table.setItem(roi_table.rowCount() - 1, 2, QTableWidgetItem(str(Max)))
            roi_table.setItem(roi_table.rowCount() - 1, 3, QTableWidgetItem(str(cx)))
            roi_table.setItem(roi_table.rowCount() - 1, 4, QTableWidgetItem(str(cy)))
            roi_table.setItem(roi_table.rowCount() - 1, 5, QTableWidgetItem(str(major)))
            roi_table.setItem(roi_table.rowCount() - 1, 6, QTableWidgetItem(str(minor)))
            roi_table.setItem(roi_table.rowCount() - 1, 7, QTableWidgetItem(str(ovality)))

        if isinstance(roi, LineRoi):
            roi_table.setColumnCount(2)
            roi_table.setHorizontalHeaderLabels(["Length", "Angle"])

            angle = roi.line().angle()
            if angle > 180:
                angle = angle - 360

            angle = round(angle, 3)

            length = round(roi.line().length(), 3)
            roi_table.setItem(roi_table.rowCount() - 1, 0, QTableWidgetItem(str(length)))
            roi_table.setItem(roi_table.rowCount() - 1, 1, QTableWidgetItem(str(angle)))

        if isinstance(roi, AngleRoi):
            roi_table.setColumnCount(1)
            roi_table.setHorizontalHeaderLabels(["Angle"])

            p1 = roi.p1.rect().center()
            p2 = roi.p2.rect().center()
            p3 = roi.p3.rect().center()

            x1 = p2.x() - p1.x()
            y1 = p2.y() - p1.y()
            x2 = p3.x() - p2.x()
            y2 = p3.y() - p2.y()
            x3 = p3.x() - p1.x()
            y3 = p3.y() - p1.y()

            l1 = math.sqrt(x1 ** 2 + y1 ** 2)
            l2 = math.sqrt(x2 ** 2 + y2 ** 2)
            l3 = math.sqrt(x3 ** 2 + y3 ** 2)

            angle = math.acos((l1 ** 2 + l2 ** 2 - l3 ** 2) / (2 * l1 * l2))

            angle = round(math.degrees(angle), 3)
            roi_table.setItem(roi_table.rowCount() - 1, 0, QTableWidgetItem(str(angle)))

        dialog.show()

    def rotate_btn_click(self):
        if self.figure.image is None:
            show_message_box("请先加载图片!")
            return
        transform = QTransform()

        dialog = QDialog(self)
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.setMinimumSize(QSize(300, 100))
        layout = QVBoxLayout(dialog)
        angle_label = QLabel("Rotation Angle")
        angle = QLineEdit()
        rotate_btn = QPushButton("Rotate")
        layout.addWidget(angle_label)
        layout.addWidget(angle)
        layout.addWidget(rotate_btn)

        def rotate():
            self.clear_button.click()
            ang = float(angle.text())
            transform.rotate(ang)
            rotated_pixmap = self.figure.pixmap_item.pixmap().transformed(transform)
            self.figure.setPixmap(rotated_pixmap)
            dialog.close()

        rotate_btn.clicked.connect(rotate)

        dialog.show()

    def save_btn_click(self):
        dialog = QDialog(self)
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.setMinimumSize(QSize(200, 100))
        layout = QVBoxLayout(dialog)
        allOrRoi = QComboBox()
        allOrRoi.addItems(["ROI", "ALL"])
        save_path_btn = QPushButton("Select storage path")
        layout.addWidget(allOrRoi)
        layout.addWidget(save_path_btn)

        def save_path_btn_click():
            file_filter = "BMP Files (*.bmp)"
            filePath, _ = QFileDialog.getSaveFileName(
                self,
                "Select storage path",
                self.last_open_dir,
                file_filter
            )
            self.last_open_dir = os.path.dirname(filePath)
            if filePath:
                if allOrRoi.currentText() == "ALL":
                    save_pixmap(filePath, self.figure.pixmap_item.pixmap())
                else:
                    if isinstance(self.figure.roi, RectangleRoi):
                        pix = self.figure.pixmap_item.pixmap().copy(self.figure.roi.rect().toRect())
                        save_pixmap(filePath, pix)
                    else:
                        show_message_box("Please select the ROI area first!")
                        return
                dialog.close()
                show_message_box("Save Successful!")

        save_path_btn.clicked.connect(save_path_btn_click)

        dialog.show()

    def find_edge_btn_click(self):
        img = self.figure.pixmap_item.pixmap().toImage()
        buffer = img.constBits()
        img = np.frombuffer(buffer, dtype='uint8').reshape((img.height(), img.width(), 4))[:, :, 0]
        # img = cv.Canny(img, 30, 200)

        # Sobel operator
        x = cv.Sobel(img, cv.CV_16S, 1, 0)
        y = cv.Sobel(img, cv.CV_16S, 0, 1)

        # Convert to uint8, image fusion
        absX = cv.convertScaleAbs(x)
        absY = cv.convertScaleAbs(y)
        img = cv.addWeighted(absX, 0.5, absY, 0.5, 0)
        self.figure.setImageNoQImage(img)


class Button(QPushButton):
    def __init__(self, icon: QIcon, string: str, roi: ROI):
        QPushButton.__init__(self, icon, string)
        self.roi = roi
