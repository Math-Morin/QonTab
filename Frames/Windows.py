#!/usr/bin/env python3

from PyQt5.QtWidgets import (
    QMainWindow,
    QStatusBar,
)

from Frames.Widgets import CentralWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("QonTab")
        self._createMenu()
        self._createStatusBar()

        self.centralWidget = CentralWidget(self)
        self.setCentralWidget(self.centralWidget)

    def _createMenu(self):
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Exit", self.close)

    def _createStatusBar(self):
        statusBar = QStatusBar()
        statusBar.showMessage("Welcome to QonTab")
        self.setStatusBar(statusBar)

