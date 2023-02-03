from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel

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
        return tableModel

    def addTransaction(self, data):
        """
        add a transaction to the database
        """
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)

        self.model.setData(self.model.index(rows,1), data[0])  # amount
        self.model.setData(self.model.index(rows,4), data[1])  # date
        self.model.setData(self.model.index(rows,5), data[2])  # description

        self.model.submitAll()
        self.model.select()