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

        currentDate = QtCore.QDate.currentDate()

        yearLabel = QLabel('Year:')
        valuesHBox.addWidget(yearLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.yearBox = QSpinBox(self)
        self.yearBox.setRange(2000,2100)
        self.yearBox.setValue(currentDate.year())
        valuesHBox.addWidget(self.yearBox)

        monthLabel = QLabel('Month:')
        valuesHBox.addWidget(monthLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.monthBox = QSpinBox(self)
        self.monthBox.setRange(0, 12)
        self.monthBox.setSpecialValueText('-')
        self.monthBox.setValue(currentDate.month())
        valuesHBox.addWidget(self.monthBox)

        dayLabel = QLabel('Day:')
        valuesHBox.addWidget(dayLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.dayBox = QSpinBox(self)
        self.dayBox.setRange(0, 31)
        self.dayBox.setSpecialValueText('-')
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
        table = self.parent.insertionsTableGroup.insertionsTable
        table.insertRow(0)

        transactorCB = QComboBox()
        transactorCB.insertItems(0, [self.transactorBox.itemText(i) for i in range(self.transactorBox.count())])
        transactorCB.setCurrentText(self.transactorBox.currentText())
        table.setCellWidget(0, 0, transactorCB)

        sharedCB = QComboBox()
        sharedCB.insertItems(0, ['no', 'yes'])
        sharedCB.setCurrentIndex(self.sharedCheckBox.checkState() == QtCore.Qt.Checked)
        table.setCellWidget(0, 1, sharedCB)

        yearSB = QSpinBox()
        yearSB.setRange(2000, 2100)
        yearSB.setValue(self.yearBox.value())
        table.setCellWidget(0, 2, yearSB)

        monthSB = QSpinBox()
        monthSB.setRange(0, 12)
        monthSB.setValue(self.monthBox.value())
        table.setCellWidget(0, 3, monthSB)

        daySB = QSpinBox()
        daySB.setRange(0, 31)
        daySB.setValue(self.dayBox.value())
        table.setCellWidget(0, 4, daySB)

        table.setItem(0, 5, QTableWidgetItem(self.transactionDescBox.text()))

        transactionTypeCB = QComboBox()
        transactionTypeCB.insertItems(0, [self.transactionTypeBox.itemText(i) for i in range(self.transactionTypeBox.count())])
        transactionTypeCB.setCurrentText(self.transactionTypeBox.currentText())
        table.setCellWidget(0, 6, transactionTypeCB)

        transactionSubtypeCB = QComboBox()
        transactionSubtypeCB.insertItems(0, [self.transactionSubtypeBox.itemText(i) for i in range(self.transactionSubtypeBox.count())])
        transactionSubtypeCB.setCurrentText(self.transactionSubtypeBox.currentText())
        table.setCellWidget(0, 7, transactionSubtypeCB)

        amountDSB = QDoubleSpinBox()
        amountDSB.setValue(self.amountBox.value())
        table.setCellWidget(0, 8, amountDSB)



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
        self.insertionsTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.insertionsTable.setHorizontalHeaderLabels(['Transactor', 'Shared?', 'Year', 'Month', 'Day', 'Decription', 'Type', 'Subtype', 'Amount'])
        self.insertionsTable.horizontalHeader().setStretchLastSection(True)
        insertionTableGridLayout.addWidget(self.insertionsTable, 0, 0, 10, 1)

        # Buttons widget
        tableButtonsWidget = QWidget(self)
        insertionTableGridLayout.addWidget(tableButtonsWidget, 10, 0, 1, 1)
        tableButtonsGridLayout = QGridLayout()
        tableButtonsWidget.setLayout(tableButtonsGridLayout)

        ## Buttons widget : buttons
        deleteRowButton = QPushButton("Delete Selected Row", self)
        deleteRowButton.setStyleSheet("background-color: orange")
        tableButtonsGridLayout.addWidget(deleteRowButton, 0, 0, 1, 1)
        clearAllInsertionsButton = QPushButton("Clear All Insertions", self)
        clearAllInsertionsButton.setStyleSheet("background-color: red")
        tableButtonsGridLayout.addWidget(clearAllInsertionsButton, 1, 0, 1, 1)
        sendToDBButton = QPushButton("Send To Database", self)
        sendToDBButton.setStyleSheet("background-color: green")
        tableButtonsGridLayout.addWidget(sendToDBButton, 0, 1, 2, 1)
