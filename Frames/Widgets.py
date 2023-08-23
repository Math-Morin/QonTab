#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

class CentralWidget(QWidget):

    def __init__(self, parent):
        super(CentralWidget, self).__init__(parent)
        self.initLayout()

    def initLayout(self):
        mainLayout = QGridLayout()
        self.setLayout(mainLayout)

        tabsWidget = QTabWidget(self)
        mainLayout.addWidget(tabsWidget, 0, 0, 2, 1)

        insertionTabWidget = QWidget(tabsWidget)
        tabsWidget.addTab(insertionTabWidget, 'Insertion')
        insertionTabLayout = QVBoxLayout()
        insertionTabWidget.setLayout(insertionTabLayout)

        defaultValuesGroup = DefaultValuesGroup('Default Values', insertionTabWidget)
        insertionTabLayout.addWidget(defaultValuesGroup)

        insertionValuesGroup = InsertionValuesGroup('Insertion Values', insertionTabWidget)
        insertionTabLayout.addWidget(insertionValuesGroup)

        recentInsertDisplayGroup = QGroupBox('Recent Insertions', insertionTabWidget)
        insertionTabLayout.addWidget(recentInsertDisplayGroup)

        visualizeTab = QWidget(self)
        tabsWidget.addTab(visualizeTab, 'Visualize')
        visualizeLayout = QFormLayout()
        visualizeTab.setLayout(visualizeLayout)
        visualizeLayout.addRow('First Name:', QLineEdit(self))
        visualizeLayout.addRow('Last Name:', QLineEdit(self))

        self.insertButton = QPushButton('Insert')
        mainLayout.addWidget(self.insertButton, 2, 0, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.insertButton = QPushButton('Clear')
        mainLayout.addWidget(self.insertButton, 2, 0, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

class DefaultValuesGroup(QGroupBox):

    def __init__(self, title, parent):
        super(QGroupBox, self).__init__(title, parent)
        self.initLayout()

    def initLayout(self):
        repeatValuesHBox = QHBoxLayout()
        self.setLayout(repeatValuesHBox)

        transactorLabel = QLabel('Transactor:')
        repeatValuesHBox.addWidget(transactorLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.transactorBox = QComboBox(self)
        self.transactorBox.setEditable(True)
        self.transactorBox.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        repeatValuesHBox.addWidget(self.transactorBox)

        yearLabel = QLabel('Year:')
        repeatValuesHBox.addWidget(yearLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.yearBox = QSpinBox(self)
        repeatValuesHBox.addWidget(self.yearBox)

        monthLabel = QLabel('Month:')
        repeatValuesHBox.addWidget(monthLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.monthBox = QComboBox(self)
        self.monthBox.addItems(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        repeatValuesHBox.addWidget(self.monthBox)

        dayLabel = QLabel('Day:')
        repeatValuesHBox.addWidget(dayLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.dayBox = QComboBox(self)
        self.dayBox.addItems([str(x) for x in range(1, 32)])
        repeatValuesHBox.addWidget(self.dayBox)

        transactionDescLabel = QLabel('Description:')
        repeatValuesHBox.addWidget(transactionDescLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.transactionDescBox = QLineEdit(self)
        repeatValuesHBox.addWidget(self.transactionDescBox)

        transactionTypeLabel = QLabel('Transaction Type:')
        repeatValuesHBox.addWidget(transactionTypeLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.transactionTypeBox = QComboBox(self)
        self.transactionTypeBox.setEditable(True)
        self.transactionTypeBox.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        repeatValuesHBox.addWidget(self.transactionTypeBox)

        transactionSubtypeLabel = QLabel('Transaction Subtype:')
        repeatValuesHBox.addWidget(transactionSubtypeLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.transactionSubtypeBox = QComboBox(self)
        self.transactionSubtypeBox.setEditable(True)
        self.transactionSubtypeBox.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        repeatValuesHBox.addWidget(self.transactionSubtypeBox)

        amountLabel = QLabel('Amount:')
        repeatValuesHBox.addWidget(amountLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.amountBox = QDoubleSpinBox(self)
        repeatValuesHBox.addWidget(self.amountBox)

        sharedLabel = QLabel('Shared?')
        repeatValuesHBox.addWidget(sharedLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.sharedCheckBox = QCheckBox(self)
        repeatValuesHBox.addWidget(self.sharedCheckBox)

class InsertionValuesGroup(QGroupBox):

    def __init__(self, title, parent):
        super(QGroupBox, self).__init__(title, parent)
        self.initLayout()

    def initLayout(self):
        repeatValuesHBox = QHBoxLayout()
        self.setLayout(repeatValuesHBox)

        transactorLabel = QLabel('Transactor:')
        repeatValuesHBox.addWidget(transactorLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.transactorBox = QComboBox(self)
        self.transactorBox.setEditable(True)
        self.transactorBox.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        repeatValuesHBox.addWidget(self.transactorBox)

        yearLabel = QLabel('Year:')
        repeatValuesHBox.addWidget(yearLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.yearBox = QSpinBox(self)
        repeatValuesHBox.addWidget(self.yearBox)

        monthLabel = QLabel('Month:')
        repeatValuesHBox.addWidget(monthLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.monthBox = QComboBox(self)
        self.monthBox.addItems(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        repeatValuesHBox.addWidget(self.monthBox)

        dayLabel = QLabel('Day:')
        repeatValuesHBox.addWidget(dayLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.dayBox = QComboBox(self)
        self.dayBox.addItems([str(x) for x in range(1, 32)])
        repeatValuesHBox.addWidget(self.dayBox)

        transactionDescLabel = QLabel('Description:')
        repeatValuesHBox.addWidget(transactionDescLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.transactionDescBox = QLineEdit(self)
        repeatValuesHBox.addWidget(self.transactionDescBox)

        transactionTypeLabel = QLabel('Transaction Type:')
        repeatValuesHBox.addWidget(transactionTypeLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.transactionTypeBox = QComboBox(self)
        self.transactionTypeBox.setEditable(True)
        self.transactionTypeBox.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        repeatValuesHBox.addWidget(self.transactionTypeBox)

        transactionSubtypeLabel = QLabel('Transaction Subtype:')
        repeatValuesHBox.addWidget(transactionSubtypeLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.transactionSubtypeBox = QComboBox(self)
        self.transactionSubtypeBox.setEditable(True)
        self.transactionSubtypeBox.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        repeatValuesHBox.addWidget(self.transactionSubtypeBox)

        amountLabel = QLabel('Amount:')
        repeatValuesHBox.addWidget(amountLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.amountBox = QDoubleSpinBox(self)
        repeatValuesHBox.addWidget(self.amountBox)

        sharedLabel = QLabel('Shared?')
        repeatValuesHBox.addWidget(sharedLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.sharedCheckBox = QCheckBox(self)
        repeatValuesHBox.addWidget(self.sharedCheckBox)
