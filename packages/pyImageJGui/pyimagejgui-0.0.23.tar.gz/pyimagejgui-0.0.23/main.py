# -*- coding: utf-8 -*-
"""
@Time : 2023/6/22 00:10
@Author : sdb20200101@gmail.com
@File: main.py
@Software : PyCharm
"""
import multiprocessing
import sys

multiprocessing.freeze_support()
from src.pyImageJGui.ui.gui import *
from qt_material import apply_stylesheet
from src.pyImageJGui.style.qssloader import style

if __name__ == "__main__":
    app = QApplication([])
    window = QMainWindow()
    window.setMinimumSize(QSize(1200, 800))
    window.setCentralWidget(ImageWidget())
    apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)
    window.setWindowTitle("PyImageJ")
    window.setStyleSheet(style)
    window.show()
    sys.exit(app.exec())
