from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from sqlalchemy.orm import Session
from sqlalchemy import select
import Database as Db

import pandas as pd


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, *args, data=None, **kwargs):
        super(TableModel, self).__init__(*args, **kwargs)
        self.data = data or pd.DataFrame

    def data(self, role=None, index=None):
        if role == Qt.DisplayRole:
            return self.data[index.row()][index.column()]

    def rowCount(self, **kwargs):
        nb_row, _ = self.data.shape
        return nb_row

    def columnCount(self, **kwargs):
        _, nb_col = self.data.shape
        return nb_col


class ListModel(QtCore.QAbstractListModel):
    def __init__(self, *args, data=None, **kwargs):
        super(ListModel, self).__init__(*args, **kwargs)
        self.data = data or pd.DataFrame()

    def data(self, role=None, index=None):
        if role == Qt.DisplayRole:
            return self.data[index.row()]

    def rowCount(self, index=None):
        nb_row, _ = self.data.shape
        return nb_row

    def populate(self, table):
        with Session(Db.engine) as session:
            for row in session.execute(select(table)):
                self.data.addItem(row[0])
