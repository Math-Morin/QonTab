from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QTabWidget,
)

from Views.InsertionTab import InsertionTab
from Views.VisualizeTab import VisualizeTab


class CentralWidget(QWidget):

    def __init__(self, parent):
        super(CentralWidget, self).__init__(parent)
        self.parent = parent

        # Layout
        centralWidgetLayout = QGridLayout(self)
        self.setLayout(centralWidgetLayout)

        # Tab widget
        tabWidget = QTabWidget(self)
        centralWidgetLayout.addWidget(tabWidget,
                                      0,  # row
                                      0,  # column
                                      2,  # rowSpan
                                      1   # columnSpan
                                      )

        # -- Insertion tab
        insertionTab = InsertionTab(tabWidget)
        tabWidget.addTab(insertionTab, 'Insertion')

        # -- Visualize tab
        visualizeTab = VisualizeTab(tabWidget)
        tabWidget.addTab(visualizeTab, 'Visualize')
