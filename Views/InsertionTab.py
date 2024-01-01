from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QGroupBox,
    QVBoxLayout,
    QTableWidget,
    QSizePolicy,
    QAbstractScrollArea,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QLineEdit,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QLabel,
    QDialog,
    QDialogButtonBox,
    QTableWidgetItem,
)
import PyQt5.QtCore as QtCore

from sqlalchemy.orm import Session
from sqlalchemy import select
import Database as Db

from pathlib import Path
import csv

from Models import Models


class InsertionTab(QWidget):
    """
    Tab under which transactions can be inserted into the database. The layout is separated into 2 groups.

    The insertion values group is displayed in the upper half of the tab. Values common to multiple transactions can be
    given here to avoid having to enter those values manually repeatedly.

    The transactions table group is displayed in the bottom half of the tab. The table displays the transactions to be
    inserted to the database. Edition is permitted.
    """

    def __init__(self, parent):
        super(InsertionTab, self).__init__(parent)

        # Data models
        self.transactorsModel = Models.ListModel()
        self.transactorsModel.populate(Db.Transactors.name)

        # Layout
        insertionTabGridLayout = QGridLayout()
        self.setLayout(insertionTabGridLayout)

        # Values Group
        self.insertionValuesGroup = InsertionValuesGroup('Default Values', self)
        insertionTabGridLayout.addWidget(self.insertionValuesGroup, 0, 0, 1, 1)

        self.transactionsTableGroup = TransactionsTableGroup('Insertions', self)
        insertionTabGridLayout.addWidget(self.transactionsTableGroup, 1, 0, 4, 1)


class InsertionValuesGroup(QGroupBox):
    def __init__(self, title, parent):
        super(InsertionValuesGroup, self).__init__(title, parent)
        self.parent = parent

        # Layout
        insertionValuesGroupVBox = QVBoxLayout()
        insertionValuesGroupVBox.setContentsMargins(50, 20, 50, 20)
        self.setLayout(insertionValuesGroupVBox)

        # Insertion Values Table
        self.insertionValuesTable = InsertionValuesTable(self)
        insertionValuesGroupVBox.addWidget(self.insertionValuesTable)

        # Buttons widget
        valuesButtonsWidget = QWidget(self)
        insertionValuesGroupVBox.addWidget(valuesButtonsWidget)
        valuesButtonsHBox = QHBoxLayout()
        valuesButtonsWidget.setLayout(valuesButtonsHBox)

        # Buttons widget : buttons
        self.importButton = QPushButton("Import from file...", self)
        self.importButton.setStyleSheet("background-color: blue")
        valuesButtonsHBox.addWidget(self.importButton)
        self.clearValuesButton = QPushButton("Clear Values", self)
        self.clearValuesButton.setStyleSheet("background-color: orange")
        valuesButtonsHBox.addWidget(self.clearValuesButton)
        self.insertRowButton = QPushButton("Insert Row", self)
        self.insertRowButton.setStyleSheet("background-color: green")
        valuesButtonsHBox.addWidget(self.insertRowButton)

        # Events
        self.importButton.clicked.connect(self.importFromFile)
        self.insertRowButton.clicked.connect(self.addRow)
        self.clearValuesButton.clicked.connect(self.clearValues)

    def importFromFile(self):
        fileName = QFileDialog.getOpenFileName(self, "Open file", str(Path(__file__).parent),
                                               "Transactions Files (*.csv)")
        self.importTransactionsFromCSV(fileName)

    def importTransactionsFromCSV(self, fileName):
        table = self.parent.transactionsTableGroup.insertionsTable

        with open(fileName) as file:
            reader = csv.reader(file, delimiter=',')
            # TODO need refactoring of this file,
            # and sharing of the cbox models as singleton

    def addRow(self):
        table = self.parent.transactionsTableGroup.insertionsTable
        table.insertRow(0)

        transactorComboBox = QComboBox()
        transactorComboBox.setModel(self.parent.transactorsModel)
        transactorComboBox.setEditable(True)
        currentTransactorName = self.insertionValuesTable.transactorComboBox.currentText().strip().title()
        transactorComboBox.addItem(currentTransactorName)
        transactorComboBox.setCurrentText(currentTransactorName)
        table.setCellWidget(0, 0, transactorComboBox)

        sharedCB = QComboBox()
        sharedCB.insertItems(0, ['no', 'yes'])
        sharedCB.setCurrentIndex(self.insertionValuesTable.sharedDefaultCB.currentIndex())
        table.setCellWidget(0, 1, sharedCB)

        yearSB = QSpinBox()
        yearSB.setRange(2000, 2100)
        yearSB.setValue(self.insertionValuesTable.yearDefaultSB.value())
        table.setCellWidget(0, 2, yearSB)

        monthSB = QSpinBox()
        monthSB.setRange(0, 12)
        monthSB.setValue(self.insertionValuesTable.monthDefaultSB.value())
        table.setCellWidget(0, 3, monthSB)

        daySB = QSpinBox()
        daySB.setRange(0, 31)
        daySB.setValue(self.insertionValuesTable.dayDefaultSB.value())
        table.setCellWidget(0, 4, daySB)

        transTypeCB = QComboBox()
        transTypeCB.insertItems(0,
                                [self.insertionValuesTable.transTypeDefaultCB.itemText(i)
                                 for i in range(self.insertionValuesTable.transTypeDefaultCB.count())])
        transTypeCB.setEditable(True)
        currentTransactorName = self.insertionValuesTable.transTypeDefaultCB.currentText().strip().title()
        transTypeCB.addItem(currentTransactorName)
        transTypeCB.setCurrentText(currentTransactorName)
        table.setCellWidget(0, 5, transTypeCB)

        transSubtypeCB = QComboBox()
        transSubtypeCB.insertItems(0,
                                   [self.insertionValuesTable.transSubtypeDefaultCB.itemText(i) for i in
                                    range(self.insertionValuesTable.transSubtypeDefaultCB.count())])
        transSubtypeCB.setEditable(True)
        currentTransactorName = self.insertionValuesTable.transSubtypeDefaultCB.currentText().strip().title()
        transSubtypeCB.addItem(currentTransactorName)
        transSubtypeCB.setCurrentText(currentTransactorName)
        table.setCellWidget(0, 6, transSubtypeCB)

        amountDSB = QDoubleSpinBox()
        amountDSB.setValue(self.insertionValuesTable.amountDefaultDSB.value())
        amountDSB.setRange(0, 99999)
        table.setCellWidget(0, 7, amountDSB)

        table.setItem(0, 8, QTableWidgetItem(self.insertionValuesTable.defaultTransactionDesc.text().strip()))

    def clearValues(self):
        self.insertionValuesTable.cellWidget(0, 0).clearEditText()
        self.insertionValuesTable.cellWidget(0, 4).setValue(0)
        self.insertionValuesTable.cellWidget(0, 5).clearEditText()
        self.insertionValuesTable.cellWidget(0, 6).clearEditText()
        self.insertionValuesTable.cellWidget(0, 7).setValue(0.0)
        self.insertionValuesTable.cellWidget(0, 8).clear()


class InsertionValuesTable(QTableWidget):
    def __init__(self, parent):
        super(InsertionValuesTable, self).__init__(parent)

        # Display
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.verticalHeader().hide()
        self.horizontalHeader().setStretchLastSection(True)

        # Format
        self.setRowCount(1)
        self.setColumnCount(9)
        self.setHorizontalHeaderLabels(['Transactor', 'Share %', 'Year', 'Month', 'Day', 'Type', 'Subtype', 'Amount',
                                        'Description'])

        # Widgets
        self.transactorComboBox = QComboBox(self)
        self.transactorComboBox.setModel(parent.parent.transactorsModel)
        self.transactorComboBox.setEditable(True)
        self.transactorComboBox.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        self.setCellWidget(0, 0, self.transactorComboBox)

        self.sharedDefaultCB = QComboBox(self)
        self.sharedDefaultCB.insertItems(0, ['no', 'yes'])
        self.setCellWidget(0, 1, self.sharedDefaultCB)

        currentDate = QtCore.QDate.currentDate()

        self.yearDefaultSB = QSpinBox(self)
        self.yearDefaultSB.setRange(2000, 2100)
        self.yearDefaultSB.setValue(currentDate.year())
        self.setCellWidget(0, 2, self.yearDefaultSB)

        self.monthDefaultSB = QSpinBox(self)
        self.monthDefaultSB.setRange(0, 12)
        self.monthDefaultSB.setSpecialValueText('-')
        self.monthDefaultSB.setValue(currentDate.month())
        self.setCellWidget(0, 3, self.monthDefaultSB)

        self.dayDefaultSB = QSpinBox(self)
        self.dayDefaultSB.setRange(0, 31)
        self.dayDefaultSB.setSpecialValueText('-')
        self.setCellWidget(0, 4, self.dayDefaultSB)

        self.transTypeDefaultCB = QComboBox(self)
        self.transTypeDefaultCB.setEditable(True)
        self.transTypeDefaultCB.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        with Session(Db.engine) as session:
            for row in session.execute(select(Db.TransactionType.maintype)):
                self.transTypeDefaultCB.addItem(row[0])
        self.setCellWidget(0, 5, self.transTypeDefaultCB)

        self.transSubtypeDefaultCB = QComboBox(self)
        self.transSubtypeDefaultCB.setEditable(True)
        self.transSubtypeDefaultCB.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        with Session(Db.engine) as session:
            for row in session.execute(select(Db.TransactionSubtype.subtype)):
                self.transSubtypeDefaultCB.addItem(row[0])
        self.setCellWidget(0, 6, self.transSubtypeDefaultCB)

        self.amountDefaultDSB = QDoubleSpinBox(self)
        self.amountDefaultDSB.setRange(0, 99999)
        self.setCellWidget(0, 7, self.amountDefaultDSB)

        self.defaultTransactionDesc = QLineEdit(self)
        self.setCellWidget(0, 8, self.defaultTransactionDesc)


class TransactionsTableGroup(QGroupBox):

    def __init__(self, title, parent):
        super(TransactionsTableGroup, self).__init__(title, parent)
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

        for row in range(self.insertionsTable.rowCount() - 1, -1, -1):
            transactor = self.insertionsTable.cellWidget(row, 0).currentText().strip().title()
            shared = self.insertionsTable.cellWidget(row, 1).currentText().strip().title()
            year = self.insertionsTable.cellWidget(row, 2).value()
            month = self.insertionsTable.cellWidget(row, 3).value()
            month = month if len(str(month)) == 2 else "0" + str(month)
            day = self.insertionsTable.cellWidget(row, 4).value()
            transaction_type = self.insertionsTable.cellWidget(row, 5).currentText().strip().title()
            transaction_subtype = self.insertionsTable.cellWidget(row, 6).currentText().strip().title()
            amount = self.insertionsTable.cellWidget(row, 7).value()
            description = self.insertionsTable.item(row, 8).text().strip()

            if transactor == '' or transaction_type == '' or description == '' or day == 0:
                continue

            with Session(Db.engine) as session:
                if not session.execute(select(Db.Transactors.name).where(Db.Transactors.name == transactor)).first():
                    session.add(Db.Transactors(name=transactor))
                if not session.execute(select(Db.TransactionType.maintype).where(
                        Db.TransactionType.maintype == transaction_type)).first():
                    session.add(Db.TransactionType(maintype=transaction_type))
                if not session.execute(select(Db.TransactionSubtype.subtype).where(
                        Db.TransactionSubtype.subtype == transaction_subtype)).first():
                    session.add(Db.TransactionSubtype(subtype=transaction_subtype))
                session.add(Db.Transactions(transactor=transactor,
                                            shared=1 if shared == "yes" else 0,
                                            date=f'{year}-{month}-{day}',
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
