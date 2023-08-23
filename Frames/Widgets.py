#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

class CentralWidget(QWidget):

    def __init__(self, parent):
        super(CentralWidget, self).__init__(parent)
        self.parent = parent
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
        self.defaultValuesGroup = DefaultValuesGroup('Default Values', self)
        insertionTabGridLayout.addWidget(self.defaultValuesGroup, 0, 0, 1, 1)
        self.insertionsTableGroup = InsertionsTableGroup('Insertions', self)
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
        self.parent = parent
        self.initLayout()
        self.initBehavior()

    def initLayout(self):
        defaultValuesGroupVBox = QVBoxLayout()
        defaultValuesGroupVBox.setContentsMargins(50, 20, 50, 20)
        self.setLayout(defaultValuesGroupVBox)

        # Values table
        self.defaultValuesTable = QTableWidget(self)
        defaultValuesGroupVBox.addWidget(self.defaultValuesTable)
        self.defaultValuesTable.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.defaultValuesTable.verticalHeader().hide()
        self.defaultValuesTable.setColumnCount(9)
        self.defaultValuesTable.setHorizontalHeaderLabels(['Transactor', 'Shared?', 'Year', 'Month', 'Day', 'Type', 'Subtype', 'Amount', 'Decription'])
        self.defaultValuesTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.defaultValuesTable.horizontalHeader().setStretchLastSection(True)
        self.defaultValuesTable.setRowCount(1)

        ## Values widget : Values
        self.transactorDefaultCB = QComboBox(self)
        self.transactorDefaultCB.setEditable(True)
        self.transactorDefaultCB.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        self.defaultValuesTable.setCellWidget(0, 0, self.transactorDefaultCB)

        self.sharedDefaultCB = QComboBox(self)
        self.sharedDefaultCB.insertItems(0, ['no', 'yes'])
        self.defaultValuesTable.setCellWidget(0, 1, self.sharedDefaultCB)

        currentDate = QtCore.QDate.currentDate()

        self.yearDefaultSB = QSpinBox(self)
        self.yearDefaultSB.setRange(2000,2100)
        self.yearDefaultSB.setValue(currentDate.year())
        self.defaultValuesTable.setCellWidget(0, 2, self.yearDefaultSB)

        self.monthDefaultSB = QSpinBox(self)
        self.monthDefaultSB.setRange(0, 12)
        self.monthDefaultSB.setSpecialValueText('-')
        self.monthDefaultSB.setValue(currentDate.month())
        self.defaultValuesTable.setCellWidget(0, 3, self.monthDefaultSB)

        self.dayDefaultSB = QSpinBox(self)
        self.dayDefaultSB.setRange(0, 31)
        self.dayDefaultSB.setSpecialValueText('-')
        self.defaultValuesTable.setCellWidget(0, 4, self.dayDefaultSB)

        self.transTypeDefaultCB = QComboBox(self)
        self.transTypeDefaultCB.setEditable(True)
        self.transTypeDefaultCB.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        self.defaultValuesTable.setCellWidget(0, 5, self.transTypeDefaultCB)

        self.transSubtypeDefaultCB = QComboBox(self)
        self.transSubtypeDefaultCB.setEditable(True)
        self.transSubtypeDefaultCB.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        self.defaultValuesTable.setCellWidget(0, 6, self.transSubtypeDefaultCB)

        self.amountDefaultDSB = QDoubleSpinBox(self)
        self.defaultValuesTable.setCellWidget(0, 7, self.amountDefaultDSB)

        self.defaultTransactionDesc = QLineEdit(self)
        self.defaultValuesTable.setCellWidget(0, 8, self.defaultTransactionDesc)

        # Buttons widget
        valuesButtonsWidget = QWidget(self)
        defaultValuesGroupVBox.addWidget(valuesButtonsWidget)
        valuesButtonsHBox = QHBoxLayout()
        valuesButtonsWidget.setLayout(valuesButtonsHBox)

        ## Buttons widget : buttons
        self.clearValuesButton = QPushButton("Clear Values", self)
        self.clearValuesButton.setStyleSheet("background-color: orange")
        valuesButtonsHBox.addWidget(self.clearValuesButton)
        self.insertRowButton = QPushButton("Insert Row", self)
        self.insertRowButton.setStyleSheet("background-color: green")
        valuesButtonsHBox.addWidget(self.insertRowButton)

    def initBehavior(self):
        self.insertRowButton.clicked.connect(self.addRow)

    def addRow(self):
        table = self.parent.insertionsTableGroup.insertionsTable
        table.insertRow(0)

        transactorCB = QComboBox()
        transactorCB.insertItems(0, [self.transactorDefaultCB.itemText(i) for i in range(self.transactorDefaultCB.count())])
        transactorCB.setCurrentText(self.transactorDefaultCB.currentText())
        table.setCellWidget(0, 0, transactorCB)

        sharedCB = QComboBox()
        sharedCB.insertItems(0, ['no', 'yes'])
        sharedCB.setCurrentIndex(self.sharedDefaultCB.currentIndex())
        table.setCellWidget(0, 1, sharedCB)

        yearSB = QSpinBox()
        yearSB.setRange(2000, 2100)
        yearSB.setValue(self.yearDefaultSB.value())
        table.setCellWidget(0, 2, yearSB)

        monthSB = QSpinBox()
        monthSB.setRange(0, 12)
        monthSB.setValue(self.monthDefaultSB.value())
        table.setCellWidget(0, 3, monthSB)

        daySB = QSpinBox()
        daySB.setRange(0, 31)
        daySB.setValue(self.dayDefaultSB.value())
        table.setCellWidget(0, 4, daySB)

        transTypeCB = QComboBox()
        transTypeCB.insertItems(0, [self.transTypeDefaultCB.itemText(i) for i in range(self.transTypeDefaultCB.count())])
        transTypeCB.setCurrentText(self.transTypeDefaultCB.currentText())
        table.setCellWidget(0, 5, transTypeCB)

        transSubtypeCB = QComboBox()
        transSubtypeCB.insertItems(0, [self.transSubtypeDefaultCB.itemText(i) for i in range(self.transSubtypeDefaultCB.count())])
        transSubtypeCB.setCurrentText(self.transSubtypeDefaultCB.currentText())
        table.setCellWidget(0, 6, transSubtypeCB)

        amountDSB = QDoubleSpinBox()
        amountDSB.setValue(self.amountDefaultDSB.value())
        table.setCellWidget(0, 7, amountDSB)

        table.setItem(0, 8, QTableWidgetItem(self.defaultTransactionDesc.text()))


class InsertionsTableGroup(QGroupBox):

    def __init__(self, title, parent):
        super(QGroupBox, self).__init__(title, parent)
        self.parent = parent
        self.initLayout()

    def initLayout(self):
        insertionTableGridLayout = QGridLayout()
        insertionTableGridLayout.setContentsMargins(50, 20, 50, 10)
        self.setLayout(insertionTableGridLayout)

        self.insertionsTable = QTableWidget(self)
        self.insertionsTable.setColumnCount(9)
        self.insertionsTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.insertionsTable.setHorizontalHeaderLabels(['Transactor', 'Shared?', 'Year', 'Month', 'Day', 'Type', 'Subtype', 'Amount', 'Decription'])
        self.insertionsTable.horizontalHeader().setStretchLastSection(True)
        insertionTableGridLayout.addWidget(self.insertionsTable, 0, 0, 10, 1)

        # Buttons widget
        tableButtonsWidget = QWidget(self)
        insertionTableGridLayout.addWidget(tableButtonsWidget, 10, 0, 1, 1)
        tableButtonsGridLayout = QGridLayout()
        tableButtonsWidget.setLayout(tableButtonsGridLayout)

        ## Buttons widget : buttons
        self.deleteRowButton = QPushButton("Delete Selected Row", self)
        self.deleteRowButton.setStyleSheet("background-color: orange")
        tableButtonsGridLayout.addWidget(self.deleteRowButton, 0, 0, 1, 1)
        self.clearAllInsertionsButton = QPushButton("Clear All Insertions", self)
        self.clearAllInsertionsButton.setStyleSheet("background-color: red")
        tableButtonsGridLayout.addWidget(self.clearAllInsertionsButton, 1, 0, 1, 1)
        self.sendToDBButton = QPushButton("Send To Database", self)
        self.sendToDBButton.setStyleSheet("background-color: green")
        self.sendToDBButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        tableButtonsGridLayout.addWidget(self.sendToDBButton, 0, 1, 2, 1)
