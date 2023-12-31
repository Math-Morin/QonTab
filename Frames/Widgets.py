#!/usr/bin/env python3

from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
import Database as DB
from pathlib import Path
import csv


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
        super(DefaultValuesGroup, self).__init__(title, parent)
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
        self.defaultValuesTable.setHorizontalHeaderLabels(['Transactor', 'Shared?', 'Year', 'Month', 'Day', 'Type',
                                                           'Subtype', 'Amount', 'Description'])
        self.defaultValuesTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.defaultValuesTable.horizontalHeader().setStretchLastSection(True)
        self.defaultValuesTable.setRowCount(1)

        ## Values widget : Values
        self.transactorDefaultCB = QComboBox(self)
        self.transactorDefaultCB.setEditable(True)
        self.transactorDefaultCB.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        with Session(DB.engine) as session:
            for row in session.execute(select(DB.Transactors.name)):
                self.transactorDefaultCB.addItem(row[0])
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
        with Session(DB.engine) as session:
            for row in session.execute(select(DB.TransactionType.maintype)):
                self.transTypeDefaultCB.addItem(row[0])
        self.defaultValuesTable.setCellWidget(0, 5, self.transTypeDefaultCB)

        self.transSubtypeDefaultCB = QComboBox(self)
        self.transSubtypeDefaultCB.setEditable(True)
        self.transSubtypeDefaultCB.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        with Session(DB.engine) as session:
            for row in session.execute(select(DB.TransactionSubtype.subtype)):
                self.transSubtypeDefaultCB.addItem(row[0])
        self.defaultValuesTable.setCellWidget(0, 6, self.transSubtypeDefaultCB)

        self.amountDefaultDSB = QDoubleSpinBox(self)
        self.amountDefaultDSB.setRange(0, 99999)
        self.defaultValuesTable.setCellWidget(0, 7, self.amountDefaultDSB)

        self.defaultTransactionDesc = QLineEdit(self)
        self.defaultValuesTable.setCellWidget(0, 8, self.defaultTransactionDesc)

        # Buttons widget
        valuesButtonsWidget = QWidget(self)
        defaultValuesGroupVBox.addWidget(valuesButtonsWidget)
        valuesButtonsHBox = QHBoxLayout()
        valuesButtonsWidget.setLayout(valuesButtonsHBox)

        ## Buttons widget : buttons
        self.importButton = QPushButton("Import from file...", self)
        self.importButton.setStyleSheet("background-color: blue")
        valuesButtonsHBox.addWidget(self.importButton)
        self.clearValuesButton = QPushButton("Clear Values", self)
        self.clearValuesButton.setStyleSheet("background-color: orange")
        valuesButtonsHBox.addWidget(self.clearValuesButton)
        self.insertRowButton = QPushButton("Insert Row", self)
        self.insertRowButton.setStyleSheet("background-color: green")
        valuesButtonsHBox.addWidget(self.insertRowButton)

    def initBehavior(self):
        self.importButton.clicked.connect(self.importFromFile)
        self.insertRowButton.clicked.connect(self.addRow)
        self.clearValuesButton.clicked.connect(self.clearValues)

    def importFromFile(self):
        fileName = QFileDialog.getOpenFileName(self, "Open file", str(Path(__file__).parent),
                                               "Transactions Files (*.csv)")
        self.importTransactionsFromCSV(fileName)

    def importTransactionsFromCSV(self, fileName):
        table = self.parent.insertionsTableGroup.insertionsTable

        with open(fileName) as file:
            reader = csv.reader(file, delimiter=',')
            # TODO need refactoring of this file,
            # and sharing of the cbox models as singleton


    def addRow(self):
        table = self.parent.insertionsTableGroup.insertionsTable
        table.insertRow(0)

        transactorCB = QComboBox()
        transactorCB.insertItems(0,
                                 [self.transactorDefaultCB.itemText(i) for i in
                                  range(self.transactorDefaultCB.count())])
        transactorCB.setEditable(True)
        item = self.transactorDefaultCB.currentText().strip().title()
        transactorCB.addItem(item)
        transactorCB.setCurrentText(item)
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
        transTypeCB.insertItems(0,
                                [self.transTypeDefaultCB.itemText(i) for i in range(self.transTypeDefaultCB.count())])
        transTypeCB.setEditable(True)
        item = self.transTypeDefaultCB.currentText().strip().title()
        transTypeCB.addItem(item)
        transTypeCB.setCurrentText(item)
        table.setCellWidget(0, 5, transTypeCB)

        transSubtypeCB = QComboBox()
        transSubtypeCB.insertItems(0,
                                   [self.transSubtypeDefaultCB.itemText(i) for i in
                                    range(self.transSubtypeDefaultCB.count())])
        transSubtypeCB.setEditable(True)
        item = self.transSubtypeDefaultCB.currentText().strip().title()
        transSubtypeCB.addItem(item)
        transSubtypeCB.setCurrentText(item)
        table.setCellWidget(0, 6, transSubtypeCB)

        amountDSB = QDoubleSpinBox()
        amountDSB.setValue(self.amountDefaultDSB.value())
        amountDSB.setRange(0, 99999)
        table.setCellWidget(0, 7, amountDSB)

        table.setItem(0, 8, QTableWidgetItem(self.defaultTransactionDesc.text().strip()))

    def clearValues(self):
        self.defaultValuesTable.cellWidget(0, 0).clearEditText()
        self.defaultValuesTable.cellWidget(0, 4).setValue(0)
        self.defaultValuesTable.cellWidget(0, 5).clearEditText()
        self.defaultValuesTable.cellWidget(0, 6).clearEditText()
        self.defaultValuesTable.cellWidget(0, 7).setValue(0.0)
        self.defaultValuesTable.cellWidget(0, 8).clear()


class InsertionsTableGroup(QGroupBox):

    def __init__(self, title, parent):
        super(InsertionsTableGroup, self).__init__(title, parent)
        self.parent = parent
        self.initLayout()

    def initLayout(self):
        insertionTableGridLayout = QGridLayout()
        insertionTableGridLayout.setContentsMargins(50, 20, 50, 10)
        self.setLayout(insertionTableGridLayout)

        self.insertionsTable = QTableWidget(self)
        self.insertionsTable.setColumnCount(9)
        self.insertionsTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.insertionsTable.setHorizontalHeaderLabels(['Transactor', 'Shared?', 'Year', 'Month', 'Day', 'Type',
                                                        'Subtype', 'Amount', 'Decription'])
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
        self.deleteRowButton.clicked.connect(self.deleteRow)
        tableButtonsGridLayout.addWidget(self.deleteRowButton, 0, 0, 1, 1)
        self.deleteAllInsertionsButton = QPushButton("Delete All Insertions", self)
        self.deleteAllInsertionsButton.setStyleSheet("background-color: red")
        self.deleteAllInsertionsButton.clicked.connect(self.deleteAllRows)
        tableButtonsGridLayout.addWidget(self.deleteAllInsertionsButton, 1, 0, 1, 1)
        self.sendToDBButton = QPushButton("Send To Database", self)
        self.sendToDBButton.setStyleSheet("background-color: green")
        self.sendToDBButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.sendToDBButton.clicked.connect(self.sendToDB)
        tableButtonsGridLayout.addWidget(self.sendToDBButton, 0, 1, 2, 1)

    def sendToDB(self):
        mainWindow = self.parent
        message = QLabel("You are about to send all rows to the database. Are you sure?")
        confirmDialog = ConfirmDeleteAllDialog(mainWindow, message)
        confirmDialog.setWindowTitle("Confirm send to database")
        if not confirmDialog.exec():
            return

        for row in range(self.insertionsTable.rowCount()-1, -1, -1):
            transactor = self.insertionsTable.cellWidget(row, 0).currentText().strip().title()
            shared = self.insertionsTable.cellWidget(row, 1).currentText().strip().title()
            year = self.insertionsTable.cellWidget(row, 2).value()
            month = self.insertionsTable.cellWidget(row, 3).value()
            month = month if len(str(month)) == 2 else "0"+str(month)
            day = self.insertionsTable.cellWidget(row, 4).value()
            transaction_type = self.insertionsTable.cellWidget(row, 5).currentText().strip().title()
            transaction_subtype = self.insertionsTable.cellWidget(row, 6).currentText().strip().title()
            amount = self.insertionsTable.cellWidget(row, 7).value()
            description = self.insertionsTable.item(row, 8).text().strip()

            if transactor == '' or transaction_type == '' or description == '' or day == 0:
                continue

            with Session(DB.engine) as session:
                if not session.execute(select(DB.Transactors.name).where(DB.Transactors.name == transactor)).first():
                    session.add(DB.Transactors(name=transactor))
                if not session.execute(select(DB.TransactionType.maintype).where(DB.TransactionType.maintype == transaction_type)).first():
                    session.add(DB.TransactionType(maintype=transaction_type))
                if not session.execute(select(DB.TransactionSubtype.subtype).where(DB.TransactionSubtype.subtype == transaction_subtype)).first():
                    session.add(DB.TransactionSubtype(subtype=transaction_subtype))
                session.add(DB.Transactions(transactor=transactor,
                                            shared = 1 if shared == "yes" else 0,
                                            date = f'{year}-{month}-{day}',
                                            transaction_type=transaction_type,
                                            transaction_subtype=transaction_subtype,
                                            amount=amount,
                                            description=description))
                session.commit()
                self.insertionsTable.removeRow(row)

    def deleteRow(self):
        indexes = [i.row() for i in self.insertionsTable.selectionModel().selectedRows()]
        for index in sorted(indexes, reverse=True):
            self.insertionsTable.removeRow(index)

    def deleteAllRows(self):
        mainWindow = self.parent

        message = QLabel("You are about to delete all rows to be inserted. Are you sure?")
        confirmDialog = ConfirmDeleteAllDialog(mainWindow, message)
        confirmDialog.setWindowTitle("Confirm delete all insertions")
        if confirmDialog.exec():
            self.insertionsTable.setRowCount(0)


class ConfirmDeleteAllDialog(QDialog):
    def __init__(self, parent=None, message=None):
        super().__init__(parent)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
