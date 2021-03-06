#!/usr/bin/env python

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class NoPath(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setGeometry(800, 1200, 200, 50)

        self.setWindowTitle("No Path Found")

        self.ok_btn = QtGui.QPushButton("Ok", self)
        self.ok_btn.clicked.connect(self.ok_clicked)
        self.ok_btn.move(60, 5)

        self.show()

    def ok_clicked(self):
        self.hide()

