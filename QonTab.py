#!/usr/bin/env python3

import sys
from Frames.Windows import MainWindow
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
