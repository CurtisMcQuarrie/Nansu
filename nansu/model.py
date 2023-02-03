from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel
from enum import Enum


class TransactionFields(Enum):
    Id = 0
    Amount = 1
    Unit = 2
    DateCreated = 3
    Date = 4
    Description = 5


class TransactionsModel:

    def __init__(self):
        self.model = self._createModel()

    @staticmethod
    def _createModel():
        """
        create and set up model
        """
        tableModel = QSqlTableModel()
        tableModel.setTable("transactions")
        tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        tableModel.select()
        headers = ("ID", "Amount", "Unit", "DateCreated", "Date", "Description")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)
        tableModel.setSort(4, Qt.AscendingOrder)
        return tableModel

    def addTransaction(self, data):
        """
        add a transaction to the database
        """
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)

        self.model.setData(self.model.index(rows,TransactionFields.Amount.value), data[0])
        self.model.setData(self.model.index(rows,TransactionFields.Date.value), data[1])
        self.model.setData(self.model.index(rows,TransactionFields.Description.value), data[2])

        self.model.submitAll()
        self.model.select()

    def deleteTransaction(self, row):
        """
        remove a transaction from the database
        """
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()

    def clearTransactions(self):
        """
        remove all transactions from the database
        """
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()