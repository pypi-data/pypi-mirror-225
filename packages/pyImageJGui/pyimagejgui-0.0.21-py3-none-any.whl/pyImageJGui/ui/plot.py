# -*- coding: utf-8 -*-
"""
@Time : 2023/8/12 17:45
@Author : sdb20200101@gmail.com
@File: plot.py
@Software : PyCharm
"""
import sys

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout
)


class PlotWidget(QWidget):
    def __init__(self, x, y=None, top=None, xlabel='', ylabel='', title='', bottom=None, marker=None, linestyle='-',
                 color='black', linewidth=None,
                 figsize=(5, 3), parent=None):
        super().__init__(parent)

        #  create widgets
        self.view = FigureCanvas(Figure(figsize=figsize))
        self.view.figure.subplots_adjust(top=top, bottom=bottom)
        self.axes = self.view.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.view, self)

        #  Create layout
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.toolbar, 10)
        vlayout.addWidget(self.view, 90)
        self.setLayout(vlayout)
        self.axes.clear()

        if y:
            self.axes.plot(x, y, marker=marker, linewidth=linewidth, linestyle=linestyle, color=color)
        else:
            self.axes.plot(x, marker=marker, linewidth=linewidth, linestyle=linestyle, color=color)
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.axes.set_title(title)
        self.view.draw()
