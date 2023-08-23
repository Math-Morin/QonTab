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

        # Insertion tab
        insertionTab = QWidget(tabsWidget)
        tabsWidget.addTab(insertionTab, 'Insertion')
        insertionTabGridLayout = QGridLayout()
        insertionTab.setLayout(insertionTabGridLayout)

        ## Insertion tab : Groups
        self.defaultValuesGroup = DefaultValuesGroup('Default Values', insertionTab)
        insertionTabGridLayout.addWidget(self.defaultValuesGroup, 0, 0, 1, 1)
        self.insertionsTableGroup = InsertionsTableGroup('Insertions', insertionTab)
        insertionTabGridLayout.addWidget(self.insertionsTableGroup, 1, 0, 4, 1)

        # Visualize tab
        visualizeTab = QWidget(tabsWidget)
        tabsWidget.addTab(visualizeTab, 'Visualize')
        visualizeTabLayout = QFormLayout()
        visualizeTab.setLayout(visualizeTabLayout)

        ## Visualize tab : Groups
        visualizeTabLayout.addRow('First Name:', QLineEdit(self))
        visualizeTabLayout.addRow('Last Name:', QLineEdit(self))


class DefaultValuesGroup(QGroupBox):

    def __init__(self, title, parent):
        super(QGroupBox, self).__init__(title, parent)
        self.initLayout()
        self.initBehavior()

    def initLayout(self):
        defaultValuesVBox = QVBoxLayout()
        defaultValuesVBox.setContentsMargins(50, 20, 50, 20)
        self.setLayout(defaultValuesVBox)

        # Values widget
        valuesWidget = QWidget(self)
        defaultValuesVBox.addWidget(valuesWidget)
        valuesHBox = QHBoxLayout()
        valuesWidget.setLayout(valuesHBox)

        ## Values widget : Values
        transactorLabel = QLabel('Transactor:')
        valuesHBox.addWidget(transactorLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.transactorBox = QComboBox(self)
        self.transactorBox.setEditable(True)
        self.transactorBox.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        valuesHBox.addWidget(self.transactorBox)

        sharedLabel = QLabel('Shared?')
        valuesHBox.addWidget(sharedLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.sharedCheckBox = QCheckBox(self)
        valuesHBox.addWidget(self.sharedCheckBox)

        yearLabel = QLabel('Year:')
        valuesHBox.addWidget(yearLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.yearBox = QSpinBox(self)
        valuesHBox.addWidget(self.yearBox)

        monthLabel = QLabel('Month:')
        valuesHBox.addWidget(monthLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.monthBox = QComboBox(self)
        self.monthBox.addItems([None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        valuesHBox.addWidget(self.monthBox)

        dayLabel = QLabel('Day:')
        valuesHBox.addWidget(dayLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.dayBox = QComboBox(self)
        self.dayBox.addItems([str(x) for x in range(1, 32)])
        valuesHBox.addWidget(self.dayBox)

        transactionDescLabel = QLabel('Description:')
        valuesHBox.addWidget(transactionDescLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.transactionDescBox = QLineEdit(self)
        valuesHBox.addWidget(self.transactionDescBox)

        transactionTypeLabel = QLabel('Trans. Type:')
        valuesHBox.addWidget(transactionTypeLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.transactionTypeBox = QComboBox(self)
        self.transactionTypeBox.setEditable(True)
        self.transactionTypeBox.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        valuesHBox.addWidget(self.transactionTypeBox)

        transactionSubtypeLabel = QLabel('Trans. Subtype:')
        valuesHBox.addWidget(transactionSubtypeLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.transactionSubtypeBox = QComboBox(self)
        self.transactionSubtypeBox.setEditable(True)
        self.transactionSubtypeBox.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        valuesHBox.addWidget(self.transactionSubtypeBox)

        amountLabel = QLabel('Amount:')
        valuesHBox.addWidget(amountLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.amountBox = QDoubleSpinBox(self)
        valuesHBox.addWidget(self.amountBox)

        # Buttons widget
        valuesButtonsWidget = QWidget(self)
        defaultValuesVBox.addWidget(valuesButtonsWidget)
        valuesButtonsHBox = QHBoxLayout()
        valuesButtonsWidget.setLayout(valuesButtonsHBox)

        ## Buttons widget : buttons
        self.clearValuesButton = QPushButton("Clear Values", self)
        valuesButtonsHBox.addWidget(self.clearValuesButton)
        self.insertRowButton = QPushButton("Insert Row", self)
        valuesButtonsHBox.addWidget(self.insertRowButton)

    def initBehavior(self):
        self.insertRowButton.clicked.connect(self.insertRow)

    def insertRow(self):
        return
        # parent.insertionsTableGroup.



class InsertionsTableGroup(QGroupBox):

    def __init__(self, title, parent):
        super(QGroupBox, self).__init__(title, parent)
        self.initLayout()

    def initLayout(self):
        insertionTableGridLayout = QGridLayout()
        insertionTableGridLayout.setContentsMargins(50, 20, 50, 10)
        self.setLayout(insertionTableGridLayout)

        insertionsTable = QTableWidget(self)
        insertionsTable.setColumnCount(7)
        insertionsTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        insertionsTable.setHorizontalHeaderLabels(['Transactor', 'Shared?', 'Date', 'Decription', 'Type', 'Subtype', 'Amount'])
        insertionsTable.horizontalHeader().setStretchLastSection(True)
        insertionTableGridLayout.addWidget(insertionsTable, 0, 0, 10, 1)

        # Buttons widget
        tableButtonsWidget = QWidget(self)
        insertionTableGridLayout.addWidget(tableButtonsWidget, 10, 0, 1, 1)
        tableButtonsHBox = QHBoxLayout()
        tableButtonsWidget.setLayout(tableButtonsHBox)

        ## Buttons widget : buttons
        clearInsertionsButton = QPushButton("Clear Insertions", self)
        tableButtonsHBox.addWidget(clearInsertionsButton)
        sendToDBButton = QPushButton("Send To Database", self)
        tableButtonsHBox.addWidget(sendToDBButton)
